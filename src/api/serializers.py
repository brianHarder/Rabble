from rest_framework import serializers
from django.contrib.auth import get_user_model
from rabble.models import SubRabble, Post

User = get_user_model()

class SubRabbleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubRabble
        fields = ['id', 'subrabble_community_id', 'subrabble_name', 'description', 'allow_anonymous', 'private', 'rabble_id']

class PostSerializer(serializers.ModelSerializer):
    user_str = serializers.StringRelatedField(source='user_id', read_only=True)
    subrabble_str = serializers.StringRelatedField(source='subrabble_id', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'user_id', 'user_str', 'subrabble_id', 'subrabble_str', 'anonymous']
