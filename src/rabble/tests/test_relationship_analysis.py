import json
import os
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from django.test import TestCase
from django.contrib.auth import get_user_model
from rabble.models import Post, PostRelationship, SubRabble, Rabble
from rabble.services import PostAnalysisService
import pytest

User = get_user_model()

class RelationshipAnalysisTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test rabble and subrabble
        self.rabble = Rabble.objects.create(
            community_id="test-rabble",
            owner=self.user,
            description="A test rabble"
        )
        self.subrabble = SubRabble.objects.create(
            subrabble_community_id="test-subrabble",
            subrabble_name="Test SubRabble",
            description="A test subrabble",
            allow_anonymous=False,
            private=False,
            rabble_id=self.rabble,
            user_id=self.user
        )
        
        # Create test posts
        self.posts = [
            Post.objects.create(
                title="Test Post 1",
                body="This is the first test post",
                user_id=self.user,
                subrabble_id=self.subrabble
            ),
            Post.objects.create(
                title="Test Post 2",
                body="This is the second test post",
                user_id=self.user,
                subrabble_id=self.subrabble
            )
        ]

    def test_relationship_creation(self):
        """Test creating a relationship between posts"""
        relationship = PostRelationship.objects.create(
            source_post=self.posts[0],
            target_post=self.posts[1],
            relationship_type='supports'
        )
        
        self.assertEqual(relationship.source_post, self.posts[0])
        self.assertEqual(relationship.target_post, self.posts[1])
        self.assertEqual(relationship.relationship_type, 'supports')

    def test_relationship_retrieval(self):
        """Test retrieving relationships for a post"""
        # Create a relationship
        PostRelationship.objects.create(
            source_post=self.posts[0],
            target_post=self.posts[1],
            relationship_type='supports'
        )
        
        # Get relationships where post1 is the source
        source_relationships = PostRelationship.objects.filter(source_post=self.posts[0])
        self.assertEqual(source_relationships.count(), 1)
        self.assertEqual(source_relationships[0].relationship_type, 'supports')
        
        # Get relationships where post1 is the target
        target_relationships = PostRelationship.objects.filter(target_post=self.posts[0])
        self.assertEqual(target_relationships.count(), 0)

    @patch('openai.AsyncOpenAI')
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    async def test_analyze_post_pair(self, mock_openai):
        """Test the analyze_post_pair method with mocked API response"""
        # Mock the API response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "supports,forward"
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_openai.return_value = mock_client
    
        service = PostAnalysisService()
        post1 = self.posts[0]
        post2 = self.posts[1]
    
        relationship, direction = await service.analyze_post_pair(post1, post2)
        
        # Verify the mock was called
        mock_client.chat.completions.create.assert_called_once()
        
        # Verify the response
        self.assertEqual(relationship, "supports")
        self.assertEqual(direction, "forward")
        
        # Verify relationship type is valid
        self.assertIn(relationship, [choice[0] for choice in PostRelationship.RELATIONSHIP_TYPES])
