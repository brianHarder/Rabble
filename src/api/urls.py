from django.urls import path
from . import views

urlpatterns = [
    path('subrabbles/', views.subrabble_list, name='api-subrabble-list'),
    path('subrabbles/!<str:subrabble_community_id>/', views.subrabble_by_identifier, name='api-subrabble'),
    path('subrabbles/!<str:subrabble_community_id>/posts/', views.post_list, name='api-post-list'),
    path('subrabbles/!<str:subrabble_community_id>/posts/<int:pk>', views.post_editor, name='api-post-editor')
]