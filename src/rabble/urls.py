from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile", views.profile, name="profile"),
    path("!<slug:subrabble_community_id>/", views.subrabble_detail, name="subrabble-detail"),
    path("new", views.subrabble_create, name="subrabble-create"),
    path("!<slug:subrabble_community_id>/edit", views.subrabble_edit, name="subrabble-edit"),
    path("!<slug:subrabble_community_id>/delete", views.subrabble_delete, name="subrabble-delete"),
    path("!<slug:subrabble_community_id>/<int:pk>/", views.post_detail, name="post-detail"),
    path("!<slug:subrabble_community_id>/new", views.post_create, name="post-create"),
    path("!<slug:subrabble_community_id>/<int:pk>/edit", views.post_edit, name="post-edit"),
    path("!<slug:subrabble_community_id>/<int:pk>/delete", views.post_delete, name="post-delete"),
    path("!<slug:subrabble_community_id>/<int:pk>/new", views.comment_create, name="comment-create"),
    path("!<slug:subrabble_community_id>/<int:post_id>/<int:pk>/edit", views.comment_edit, name="comment-edit"),
    path("!<slug:subrabble_community_id>/<int:post_id>/<int:pk>/delete", views.comment_delete, name="comment-delete"),
]