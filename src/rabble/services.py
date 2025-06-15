import openai
import environ
from django.conf import settings
from .models import Post, PostRelationship
from typing import Optional, Tuple
import asyncio
from django.core.exceptions import ImproperlyConfigured
from asgiref.sync import sync_to_async

env = environ.Env()

class PostAnalysisService:
    _instance = None
    _api_key = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PostAnalysisService, cls).__new__(cls)
            # Initialize API key once
            try:
                cls._api_key = env('OPENAI_API_KEY')
                if not cls._api_key:
                    raise ImproperlyConfigured('OPENAI_API_KEY environment variable is not set')
            except Exception as e:
                raise ImproperlyConfigured(f'Failed to load OPENAI_API_KEY: {str(e)}')
        return cls._instance

    def __init__(self):
        # Ensure API key is set
        if not self._api_key:
            raise ImproperlyConfigured('OpenAI API key not initialized')

    async def analyze_post_pair(self, post1: Post, post2: Post) -> Tuple[str, str]:
        """
        Analyze the relationship between two posts using OpenAI API.
        Returns a tuple of (relationship_type, direction)
        where direction is either 'forward' or 'reverse'
        """
        # Set API key from singleton instance
        client = openai.AsyncOpenAI(api_key=self._api_key)
        
        prompt = f"""Analyze the relationship between these two posts and categorize it as one of the following:
- contradicts
- supports
- elaborates
- questions
- shifts_focus
- none

Post 1:
Title: {post1.title}
Content: {post1.body}

Post 2:
Title: {post2.title}
Content: {post2.body}

Respond with the category name followed by the direction, separated by a comma.
For example: "contradicts,forward" means Post 1 contradicts Post 2.
If there is no relationship, respond with "none,forward"."""

        try:
            response = await client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": "You are a precise relationship analyzer. Your task is to categorize the relationship between two posts into one of these categories: contradicts, supports, elaborates, questions, shifts_focus, or none. Always respond with exactly two words separated by a comma: the category and the direction (forward or reverse)."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=20
            )
            
            result = response.choices[0].message.content.strip().lower()
            relationship, direction = result.split(',')
            
            # Ensure relationship matches model choices
            if relationship not in [choice[0] for choice in PostRelationship.RELATIONSHIP_TYPES]:
                relationship = 'none'
            
            return relationship, direction
            
        except Exception as e:
            print(f"Error analyzing posts: {e}")
            return "none", "forward"

    @sync_to_async
    def get_posts(self, subrabble_id: Optional[int] = None):
        """Get posts for a subrabble or all posts"""
        if subrabble_id:
            posts = Post.objects.filter(subrabble_id=subrabble_id)
            if not posts.exists():
                raise ValueError(f"No posts found in subrabble with ID {subrabble_id}")
        else:
            posts = Post.objects.all()
        return list(posts)

    @sync_to_async
    def relationship_exists(self, post1: Post, post2: Post) -> bool:
        """Check if a relationship already exists between two posts"""
        return PostRelationship.objects.filter(
            source_post=post1,
            target_post=post2
        ).exists()

    @sync_to_async
    def create_relationship(self, source: Post, target: Post, relationship_type: str):
        """Create a new relationship between posts"""
        PostRelationship.objects.create(
            source_post=source,
            target_post=target,
            relationship_type=relationship_type
        )

    async def analyze_all_posts(self, subrabble_id: Optional[int] = None):
        """
        Analyze all pairs of posts in a subrabble or across all posts
        """
        try:
            posts = await self.get_posts(subrabble_id)
            total_pairs = len(posts) * (len(posts) - 1) // 2
            processed_pairs = 0
            
            for i in range(len(posts)):
                for j in range(i + 1, len(posts)):
                    post1, post2 = posts[i], posts[j]
                    
                    # Skip if relationship already exists
                    if await self.relationship_exists(post1, post2):
                        continue
                    
                    relationship, direction = await self.analyze_post_pair(post1, post2)
                    
                    if relationship != "none":
                        if direction == "forward":
                            source, target = post1, post2
                        else:  # reverse
                            source, target = post2, post1
                            
                        await self.create_relationship(source, target, relationship)
                    
                    processed_pairs += 1
                    if processed_pairs % 10 == 0:
                        print(f"Processed {processed_pairs}/{total_pairs} pairs")
        except Exception as e:
            raise ValueError(f"Error analyzing posts: {str(e)}")