from django.urls import path
from . import views

urlpatterns = [
    path('rabbles/<slug:community_id>/subrabbles/', views.subrabble_list, name='api-subrabble-list'),
    path('rabbles/<slug:community_id>/subrabbles/!<str:subrabble_community_id>/', views.subrabble_by_identifier, name='api-subrabble'),
    path('rabbles/<slug:community_id>/subrabbles/!<str:subrabble_community_id>/posts/', views.post_list, name='api-post-list'),
    path('rabbles/<slug:community_id>/subrabbles/!<str:subrabble_community_id>/posts/<int:pk>', views.post_editor, name='api-post-editor'),
    path('rabbles/<slug:community_id>/subrabbles/!<str:subrabble_community_id>/posts/<int:pk>/likes/', views.post_likes, name='post-likes'),
    path('rabbles/<slug:community_id>/subrabbles/!<str:subrabble_community_id>/posts/<int:post_id>/comments/<int:pk>', views.comment_editor, name='api-comment-editor'),
]