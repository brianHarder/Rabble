from django.contrib import admin
from .models import (
    User, Rabble, SubRabble, Chat, Interest, Message,
    Post, Comment, PostLike, CommentLike
)

admin.site.register(User)
admin.site.register(Rabble)
admin.site.register(SubRabble)
admin.site.register(Chat)
admin.site.register(Interest)
admin.site.register(Message)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostLike)
admin.site.register(CommentLike)
