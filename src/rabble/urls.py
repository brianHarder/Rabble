from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile", views.profile, name="profile"),
    path("!<slug:subrabble_community_id>/", views.subrabble_detail, name="subrabble-detail"),
    path("!<slug:subrabble_community_id>/<int:pk>/", views.post_detail, name="post-detail"),
    path("!<slug:subrabble_community_id>/new", views.post_create, name="post-create"),
    path("!<slug:subrabble_community_id>/<int:pk>/edit", views.post_edit, name="post-edit"),
]