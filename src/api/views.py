from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rabble.models import Post, PostRelationship
from rabble.services import PostAnalysisService
import asyncio

from rabble.models import *
from .serializers import *

@api_view(['GET', 'PATCH'])
def rabble_by_identifier(request, community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)

    if request.method == "GET":
        serializer = RabbleSerializer(rabble)
        return Response(serializer.data)
    
    elif request.method == "PATCH":
        # Check if user is the owner
        if request.user != rabble.owner:
            return Response({"error": "You cannot edit this Rabble."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = RabbleSerializer(rabble, data=request.data, partial=True)
        if serializer.is_valid():
            if 'community_id' in request.data and request.data['community_id'] != rabble.community_id:
                new_community_id = request.data['community_id']
                
                if not new_community_id.replace('-', '').isalnum():
                    return Response(
                        {"community_id": ["Community ID can only contain letters, numbers, and dashes."]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
               
                if Rabble.objects.filter(community_id=new_community_id).exists():
                    return Response(
                        {"community_id": ["This community ID is already taken."]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Handle members if provided
            if 'members' in request.data:
                members = request.data.pop('members')
                rabble.members.set(members)
            
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH'])
def subrabble_by_identifier(request, community_id, subrabble_community_id):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)

    if request.method == "GET":
        serializer = SubRabbleSerializer(subrabble)
        return Response(serializer.data)
    
    elif request.method == "PATCH":
        # Check if user is the owner
        if request.user != subrabble.user_id:
            return Response({"error": "You cannot edit this SubRabble."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = SubRabbleSerializer(subrabble, data=request.data, partial=True)
        if serializer.is_valid():
            # If community_id is being changed, we need to handle it specially
            if 'subrabble_community_id' in request.data and request.data['subrabble_community_id'] != subrabble.subrabble_community_id:
                new_community_id = request.data['subrabble_community_id']
               
                if not new_community_id.replace('-', '').isalnum():
                    return Response(
                        {"subrabble_community_id": ["Community ID can only contain letters, numbers, and dashes."]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                if SubRabble.objects.filter(subrabble_community_id=new_community_id).exists():
                    return Response(
                        {"subrabble_community_id": ["This community ID is already taken."]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
           
            if 'members' in request.data:
                members = request.data.pop('members')
                subrabble.members.set(members)
            
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PATCH', 'DELETE'])
def post_editor(request, community_id, subrabble_community_id, pk):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)
    post = get_object_or_404(Post, pk=pk, subrabble_id=subrabble)

    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    elif request.method == "PATCH":
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['POST'])
def post_likes(request, community_id, subrabble_community_id, pk):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)
    post = get_object_or_404(Post, pk=pk, subrabble_id=subrabble)

    username = request.data.get('user')
    if not username:
        return Response(
            {"detail": "Missing required field: user"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    user = get_object_or_404(User, username=username)

    existing = PostLike.objects.filter(user=user, post=post)
    if existing.exists():
        existing.delete()
        liked = False
    else:
        PostLike.objects.create(user=user, post=post)
        liked = True

    like_count = post.post_likes.count()

    return Response(
        {
            "liked": liked,
            "like_count": like_count
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET', 'PATCH', 'DELETE'])
def comment_editor(request, community_id, subrabble_community_id, post_id, pk):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)
    post = get_object_or_404(Post, pk=post_id, subrabble_id=subrabble)
    comment = get_object_or_404(Comment, pk=pk, post_id=post)

    if request.method == "GET":
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    elif request.method == "PATCH":
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['POST'])
def comment_likes(request, community_id, subrabble_community_id, post_id, pk):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)
    post = get_object_or_404(Post, pk=post_id, subrabble_id=subrabble)
    comment = get_object_or_404(Comment, pk=pk, post_id=post)

    username = request.data.get('user')
    if not username:
        return Response(
            {"detail": "Missing required field: user"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    user = get_object_or_404(User, username=username)

    existing = CommentLike.objects.filter(user=user, comment=comment)
    if existing.exists():
        existing.delete()
        liked = False
    else:
        CommentLike.objects.create(user=user, comment=comment)
        liked = True

    like_count = comment.comment_likes.count()

    return Response(
        {
            "liked": liked,
            "like_count": like_count
        },
        status=status.HTTP_200_OK
    )

@csrf_exempt
@api_view(['POST'])
def comment_dislikes(request, community_id, subrabble_community_id, post_id, pk):
    rabble = get_object_or_404(Rabble, community_id=community_id)
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id, rabble_id=rabble)
    post = get_object_or_404(Post, pk=post_id, subrabble_id=subrabble)
    comment = get_object_or_404(Comment, pk=pk, post_id=post)

    username = request.data.get('user')
    if not username:
        return Response(
            {"detail": "Missing required field: user"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    user = get_object_or_404(User, username=username)

    existing = CommentLike.objects.filter(user=user, comment=comment, is_dislike=True)
    if existing.exists():
        existing.delete()
        disliked = False
    else:
        CommentLike.objects.filter(user=user, comment=comment, is_dislike=False).delete()
        CommentLike.objects.create(user=user, comment=comment, is_dislike=True)
        disliked = True

    dislike_count = CommentLike.objects.filter(comment=comment, is_dislike=True).count()

    return Response(
        {
            "disliked": disliked,
            "dislike_count": dislike_count
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
def analyze_relationships(request):
    """
    Trigger analysis of post relationships
    POST /api/relationships/analyze/
    Body: {
        "subrabble_id": int (optional)
    }
    """
    subrabble_id = request.data.get('subrabble_id')
    
    if not subrabble_id:
        return Response({'error': 'subrabble_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        service = PostAnalysisService()
        loop.run_until_complete(service.analyze_all_posts(subrabble_id))
        return Response({'status': 'analysis completed'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        loop.close()

@api_view(['GET'])
def relationship_web(request):
    """
    Get the relationship web for a set of posts
    GET /api/relationships/web/
    Query params:
        - post_ids: comma-separated list of post IDs
        - subrabble_id: ID of subrabble to get all posts from
        - relationship_types: comma-separated list of relationship types to include
    """
    post_ids = request.query_params.get('post_ids', '').split(',')
    subrabble_id = request.query_params.get('subrabble_id')
    relationship_types = request.query_params.get('relationship_types', '').split(',')
    
    if subrabble_id:
        posts = Post.objects.filter(subrabble_id=subrabble_id)
    elif post_ids and post_ids[0]:
        posts = Post.objects.filter(id__in=post_ids)
    else:
        return Response({'error': 'Must provide either post_ids or subrabble_id'}, 
                      status=status.HTTP_400_BAD_REQUEST)
    
    relationships = PostRelationship.objects.filter(
        source_post__in=posts,
        target_post__in=posts
    )
    
    if relationship_types and relationship_types[0]:
        relationships = relationships.filter(relationship_type__in=relationship_types)
    
    nodes = [{
        'id': post.id,
        'title': post.title,
        'type': 'post'
    } for post in posts]
    
    edges = [{
        'source': rel.source_post.id,
        'target': rel.target_post.id,
        'type': rel.relationship_type
    } for rel in relationships]
    
    return Response({
        'nodes': nodes,
        'edges': edges
    })

@api_view(['GET'])
def post_relationships(request, post_id):
    """
    Get all relationships for a specific post
    GET /api/relationships/{post_id}/
    """
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    outgoing = PostRelationship.objects.filter(source_post=post)
    incoming = PostRelationship.objects.filter(target_post=post)
    
    data = {
        'outgoing': [{
            'target_post_id': rel.target_post.id,
            'target_post_title': rel.target_post.title,
            'relationship_type': rel.relationship_type
        } for rel in outgoing],
        'incoming': [{
            'source_post_id': rel.source_post.id,
            'source_post_title': rel.source_post.title,
            'relationship_type': rel.relationship_type
        } for rel in incoming]
    }
    
    return Response(data)
