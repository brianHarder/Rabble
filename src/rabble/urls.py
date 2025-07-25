from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("forgot-password/", views.forgot_password, name="forgot-password"),
    path("create/", views.rabble_create, name="rabble-create"),
    path("<slug:community_id>/", views.rabble_detail, name="rabble-detail"),
    path("<slug:community_id>/edit/", views.rabble_edit, name="rabble-edit"),
    path("<slug:community_id>/delete/", views.rabble_delete, name="rabble-delete"),
    path("<slug:community_id>/!<slug:subrabble_community_id>/", views.subrabble_detail, name="subrabble-detail"),
    path("<slug:community_id>/new/", views.subrabble_create, name="subrabble-create"),
    path("<slug:community_id>/!<slug:subrabble_community_id>/edit/", views.subrabble_edit, name="subrabble-edit"),
    path("<slug:community_id>/!<slug:subrabble_community_id>/delete/", views.subrabble_delete, name="subrabble-delete"),
    path("<slug:community_id>/!<slug:subrabble_community_id>/<int:pk>/", views.post_detail, name="post-detail"),
    path("<slug:community_id>/!<slug:subrabble_community_id>/create/", views.post_create, name="post-create"),
    path("<slug:community_id>/!<slug:subrabble_community_id>/<int:pk>/edit/", views.post_edit, name="post-edit"),
    path("<slug:community_id>/!<slug:subrabble_community_id>/<int:pk>/delete/", views.post_delete, name="post-delete"),
    path("<slug:community_id>/!<slug:subrabble_community_id>/<int:pk>/comment/", views.comment_create, name="comment-create"),
    path("<slug:community_id>/!<slug:subrabble_community_id>/<int:post_id>/<int:pk>/edit/", views.comment_edit, name="comment-edit"),
    path("<slug:community_id>/!<slug:subrabble_community_id>/<int:post_id>/<int:pk>/delete/", views.comment_delete, name="comment-delete"),
]