from django.db import models
from django.contrib.auth.models import User
from blogs.models import Blog


class Comment(models.Model):
    """
    Reader and author discussion comment on a blog post.
    """
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Blog Post"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_comments',
        verbose_name="User"
    )
    content = models.TextField(
        max_length=2000,
        verbose_name="Comment Content"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['blog', '-created_date'], name='comment_blog_created_idx'),
        ]

    def __str__(self):
        return f"Comment by {self.user.username} on '{self.blog.title}'"


class Like(models.Model):
    """
    Like reaction for a blog post.
    Enforces strictly one like per user per blog.
    """
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="Blog Post"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_likes',
        verbose_name="User"
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        constraints = [
            models.UniqueConstraint(
                fields=['blog', 'user'],
                name='unique_user_blog_like'
            )
        ]
        indexes = [
            models.Index(fields=['blog', 'user'], name='like_blog_user_idx'),
        ]

    def __str__(self):
        return f"{self.user.username} likes '{self.blog.title}'"


class Bookmark(models.Model):
    """
    Saved article bookmark for later reading.
    Enforces strictly one bookmark per user per blog.
    """
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name="Blog Post"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_bookmarks',
        verbose_name="User"
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"
        constraints = [
            models.UniqueConstraint(
                fields=['blog', 'user'],
                name='unique_user_blog_bookmark'
            )
        ]
        indexes = [
            models.Index(fields=['user', '-created_date'], name='bookmark_user_created_idx'),
        ]

    def __str__(self):
        return f"{self.user.username} bookmarked '{self.blog.title}'"
