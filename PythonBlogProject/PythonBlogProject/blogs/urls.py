from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.blog_list_view, name='blog_list'),
    path('categories/', views.category_list_view, name='category_list'),
    path('tags/<slug:slug>/', views.tag_detail_view, name='tag_detail'),
    path('create/', views.blog_create_view, name='blog_create'),
    path('my-blogs/', views.my_blogs_view, name='my_blogs'),
    path('<slug:slug>/', views.blog_detail_view, name='blog_detail'),
    path('<slug:slug>/edit/', views.blog_update_view, name='blog_update'),
    path('<slug:slug>/delete/', views.blog_delete_view, name='blog_delete'),
]
