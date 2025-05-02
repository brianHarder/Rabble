from rest_framework import serializers
from rabble.models import *

class SubRabbleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubRabble
        fields = ['id', 'subrabble_community_id', 'subrabble_name', 'description', 'allow_anonymous', 'private', 'rabble_id']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'user_id', 'subrabble_id', 'anonymous']