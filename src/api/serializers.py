from rest_framework import serializers
from rabble.models import SubRabble, Post, User

class SubRabbleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubRabble
        fields = ['id', 'subrabble_community_id', 'subrabble_name', 'description', 'allow_anonymous', 'private', 'rabble_id']

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
