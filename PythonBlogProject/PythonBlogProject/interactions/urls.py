from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    path('comment/<int:blog_id>/', views.add_comment_view, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment_view, name='delete_comment'),
    path('like/<int:blog_id>/', views.toggle_like_view, name='toggle_like'),
    path('bookmark/<int:blog_id>/', views.toggle_bookmark_view, name='toggle_bookmark'),
    path('bookmarks/', views.bookmarks_list_view, name='bookmarks_list'),
]
