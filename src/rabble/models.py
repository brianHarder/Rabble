from django.db import models
from django.contrib.auth.models import AbstractUser

class Rabble(models.Model):
    community_id = models.TextField(unique=True)
    subrabble_id = models.IntegerField()  # should be foreign? or not needed?
    chat_id = models.IntegerField()

class SubRabble(models.Model):
    subrabble_community_id = models.TextField()
    allow_anonymous = models.BooleanField()
    description = models.TextField()
    privacy = models.BooleanField()
    rabble_id = models.ForeignKey(Rabble, on_delete=models.CASCADE)

class Chat(models.Model):
    rabble_id = models.ForeignKey(Rabble, on_delete=models.CASCADE)

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True)

    follows = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    invites = models.ManyToManyField('self', symmetrical=False, related_name='invitations')
    joined_rabbles = models.ManyToManyField(Rabble)
    joined_subrabbles = models.ManyToManyField(SubRabble)
    added_to_chat = models.ManyToManyField(Chat)
    interested_in = models.ManyToManyField('Interest')

class Interest(models.Model):
    name = models.TextField(unique=True)

class Message(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user_id', 'chat_id']

class Post(models.Model):
    title = models.TextField(blank=True, null=True)
    body = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    subrabble_id = models.ForeignKey(SubRabble, on_delete=models.CASCADE)

    post_likes = models.ManyToManyField(User, through='PostLike', related_name="liked_posts")

class Comment(models.Model):
    parent_id = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()

    comment_likes = models.ManyToManyField(User, through='CommentLike', related_name="liked_comments")

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_dislike = models.BooleanField()

    class Meta:
        unique_together = ['user', 'post']

class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    is_dislike = models.BooleanField()

    class Meta:
        unique_together = ['user', 'comment']
