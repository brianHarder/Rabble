from django.urls import path
from . import views

urlpatterns = [
    path('rabbles/<slug:community_id>/subrabbles/!<str:subrabble_community_id>/', views.subrabble_by_identifier, name='api-subrabble'),
    path('rabbles/<slug:community_id>/subrabbles/!<str:subrabble_community_id>/posts/<int:pk>', views.post_editor, name='api-post-editor'),
    path('rabbles/<slug:community_id>/subrabbles/!<str:subrabble_community_id>/posts/<int:pk>/likes/', views.post_likes, name='post-likes'),
    path('rabbles/<slug:community_id>/subrabbles/!<str:subrabble_community_id>/posts/<int:post_id>/comments/<int:pk>/likes/', views.comment_likes, name='comment-likes'),
    path('rabbles/<slug:community_id>/subrabbles/!<str:subrabble_community_id>/posts/<int:post_id>/comments/<int:pk>/dislikes/', views.comment_dislikes, name='comment-dislikes'),
    path('rabbles/<slug:community_id>/subrabbles/!<str:subrabble_community_id>/posts/<int:post_id>/comments/<int:pk>', views.comment_editor, name='api-comment-editor'),
    path('rabbles/<slug:community_id>/', views.rabble_by_identifier, name='api-rabble'),
    path('relationships/analyze/', views.analyze_relationships, name='analyze-relationships'),
    path('relationships/web/', views.relationship_web, name='relationship-web'),
    path('relationships/<int:post_id>/', views.post_relationships, name='post-relationships'),
]