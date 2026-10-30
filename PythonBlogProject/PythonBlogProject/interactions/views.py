from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.http import require_POST

from blogs.models import Blog
from .models import Comment, Like, Bookmark
from .forms import CommentForm


@login_required
@require_POST
def add_comment_view(request, blog_id):
    """
    Adds a new comment to a published blog post.
    """
    blog = get_object_or_404(Blog, pk=blog_id, status='published')
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.blog = blog
        comment.user = request.user
        comment.save()
        messages.success(request, "Your comment has been posted!")
    else:
        for error in form.errors.get('content', []):
            messages.error(request, error)

    return redirect(f"{blog.get_absolute_url() if hasattr(blog, 'get_absolute_url') else '/blogs/' + blog.slug + '/'}#comments")


@login_required
@require_POST
def delete_comment_view(request, comment_id):
    """
    Deletes a comment.
    Permission check: strictly allowed only if user is comment author OR blog author.
    """
    comment = get_object_or_404(Comment.objects.select_related('blog'), pk=comment_id)
    blog_slug = comment.blog.slug

    # Permission check: comment author or blog owner
    if request.user != comment.user and request.user != comment.blog.author:
        raise PermissionDenied("You do not have permission to delete someone else's comment.")

    comment.delete()
    messages.success(request, "Comment deleted successfully.")
    return redirect(f"/blogs/{blog_slug}/#comments")


@login_required
@require_POST
def toggle_like_view(request, blog_id):
    """
    Toggles a like reaction on a published blog post.
    Enforces one like per user per blog.
    """
    blog = get_object_or_404(Blog, pk=blog_id, status='published')

    like = Like.objects.filter(blog=blog, user=request.user).first()
    if like:
        like.delete()
        messages.info(request, "You unliked this article.")
    else:
        Like.objects.create(blog=blog, user=request.user)
        messages.success(request, "You liked this article!")

    return redirect(f"/blogs/{blog.slug}/#reactions")


@login_required
@require_POST
def toggle_bookmark_view(request, blog_id):
    """
    Toggles bookmarking of a published blog post for reading later.
    """
    blog = get_object_or_404(Blog, pk=blog_id, status='published')
    next_url = request.POST.get('next') or f"/blogs/{blog.slug}/"

    bookmark = Bookmark.objects.filter(blog=blog, user=request.user).first()
    if bookmark:
        bookmark.delete()
        messages.info(request, "Removed article from your saved bookmarks.")
    else:
        Bookmark.objects.create(blog=blog, user=request.user)
        messages.success(request, "Article saved to your bookmarks!")

    return redirect(next_url)


@login_required
def bookmarks_list_view(request):
    """
    Displays the authenticated user's saved bookmarks with pagination.
    """
    bookmarks_qs = Bookmark.objects.filter(
        user=request.user,
        blog__status='published'
    ).select_related(
        'blog', 'blog__author', 'blog__author__profile', 'blog__category'
    ).prefetch_related('blog__tags').order_by('-created_date')

    paginator = Paginator(bookmarks_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'interactions/bookmarks_list.html', {
        'page_obj': page_obj,
        'bookmarks': page_obj.object_list,
        'total_bookmarks': paginator.count,
    })
