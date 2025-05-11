from django.db import models
from django.contrib.auth.models import AbstractUser

class Rabble(models.Model):
    community_id = models.TextField(unique=True)
    owner = models.ForeignKey('User', on_delete=models.CASCADE)

class SubRabble(models.Model):
    subrabble_community_id = models.CharField(max_length=200, unique=True)
    subrabble_name = models.CharField(max_length=200)
    description = models.TextField()
    allow_anonymous = models.BooleanField()
    private = models.BooleanField()
    rabble_id = models.ForeignKey(Rabble, on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.subrabble_community_id

class Chat(models.Model):
    rabble_id = models.ForeignKey(Rabble, on_delete=models.CASCADE)

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True)

    follows = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    invites = models.ManyToManyField('self', symmetrical=False, related_name='invitations', blank=True)
    joined_rabbles = models.ManyToManyField(Rabble, blank=True)
    joined_subrabbles = models.ManyToManyField(SubRabble, blank=True)
    added_to_chat = models.ManyToManyField(Chat, blank=True)
    interested_in = models.ManyToManyField('Interest', blank=True)

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
    title = models.CharField(max_length=500)
    body = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    subrabble_id = models.ForeignKey(SubRabble, on_delete=models.CASCADE)
    anonymous = models.BooleanField(default=False)

    post_likes = models.ManyToManyField(User, through='PostLike', related_name="liked_posts", blank=True)

class Comment(models.Model):
    parent_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    anonymous = models.BooleanField(default=False)

    comment_likes = models.ManyToManyField(User, through='CommentLike', related_name="liked_comments", blank=True)

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_dislike = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'post']

class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    is_dislike = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'comment']
