from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rabble.models import *
from .serializers import *

@api_view(['GET'])
def subrabble_list(request):
    if request.method == "GET":
        subrabbles = SubRabble.objects.all()
        serializer = SubRabbleSerializer(subrabbles, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def subrabble_by_identifier(request, subrabble_community_id):
    if request.method == "GET":
        subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id)
        serializer = SubRabbleSerializer(subrabble)
        return Response(serializer.data)
    
@api_view(['GET', 'POST'])
def post_list(request, subrabble_community_id):
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id)

    if request.method == "GET":
        posts = Post.objects.filter(subrabble_id=subrabble)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PATCH', 'DELETE'])
def post_editor(request, subrabble_community_id, pk):
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id)
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
def post_likes(request, subrabble_community_id, pk):
    subrabble = get_object_or_404(SubRabble, subrabble_community_id=subrabble_community_id)
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
