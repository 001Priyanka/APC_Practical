from django.contrib import admin
from .models import Comment, Like, Bookmark


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'created_date', 'short_content')
    list_filter = ('created_date',)
    search_fields = ('content', 'user__username', 'blog__title')
    readonly_fields = ('created_date', 'updated_date')

    @admin.display(description='Content Excerpt')
    def short_content(self, instance):
        return instance.content[:60] + ('...' if len(instance.content) > 60 else '')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('user__username', 'blog__title')
    readonly_fields = ('created_date',)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('user__username', 'blog__title')
    readonly_fields = ('created_date',)
