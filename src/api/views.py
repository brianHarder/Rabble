from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

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
            # If community_id is being changed, we need to handle it specially
            if 'community_id' in request.data and request.data['community_id'] != rabble.community_id:
                new_community_id = request.data['community_id']
                # Check if the new community_id is valid
                if not new_community_id.replace('-', '').isalnum():
                    return Response(
                        {"community_id": ["Community ID can only contain letters, numbers, and dashes."]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                # Check if the new community_id is already taken
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
                # Check if the new community_id is valid
                if not new_community_id.replace('-', '').isalnum():
                    return Response(
                        {"subrabble_community_id": ["Community ID can only contain letters, numbers, and dashes."]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                # Check if the new community_id is already taken
                if SubRabble.objects.filter(subrabble_community_id=new_community_id).exists():
                    return Response(
                        {"subrabble_community_id": ["This community ID is already taken."]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Handle members if provided
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
