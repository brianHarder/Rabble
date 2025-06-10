from rest_framework import serializers
from rabble.models import SubRabble, Post, User, Comment, Rabble

class RabbleSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Rabble
        fields = ['id', 'community_id', 'description', 'private', 'members']

class SubRabbleSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = SubRabble
        fields = ['id', 'subrabble_community_id', 'subrabble_name', 'description', 'allow_anonymous', 'private', 'rabble_id', 'members']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        source='user_id',
        slug_field='username',
        queryset=User.objects.all()
    )
   
    subrabble = serializers.SlugRelatedField(
        source='subrabble_id',
        slug_field='subrabble_community_id',
        queryset=SubRabble.objects.all()
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'subrabble', 'anonymous']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        source='user_id',
        slug_field='username',
        queryset=User.objects.all()
    )
   
    post = serializers.PrimaryKeyRelatedField(
        source='post_id',
        queryset=Post.objects.all()
    )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'anonymous']
