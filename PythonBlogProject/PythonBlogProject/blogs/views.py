from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import Http404
from django.db.models import Q, Count

from .models import Blog, Category, Tag
from .forms import BlogPostForm
from interactions.forms import CommentForm


def blog_list_view(request):
    """
    Public feed of published blogs.
    Supports search query, category filtering, tag filtering, and pagination.
    """
    search_query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    tag_slug = request.GET.get('tag', '').strip()

    blogs_qs = Blog.objects.filter(status='published').select_related(
        'author', 'author__profile', 'category'
    ).prefetch_related('tags').order_by('-created_date', '-id')

    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        blogs_qs = blogs_qs.filter(category=active_category)

    active_tag = None
    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        blogs_qs = blogs_qs.filter(tags=active_tag)

    if search_query:
        blogs_qs = blogs_qs.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()

    # Pagination: 6 blogs per page
    paginator = Paginator(blogs_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Categories and popular tags for sidebar filter
    categories = Category.objects.annotate(
        published_count=Count('blogs', filter=Q(blogs__status='published'))
    ).filter(published_count__gt=0).order_by('name')

    popular_tags = Tag.objects.annotate(
        published_count=Count('blogs', filter=Q(blogs__status='published'))
    ).filter(published_count__gt=0).order_by('-published_count')[:15]

    return render(request, 'blogs/blog_list.html', {
        'page_obj': page_obj,
        'blogs': page_obj.object_list,
        'search_query': search_query,
        'active_category': active_category,
        'active_tag': active_tag,
        'categories': categories,
        'popular_tags': popular_tags,
        'total_published': paginator.count,
    })


def category_list_view(request):
    """
    Public directory of editorial categories.
    Lists categories with published post counts and descriptions.
    """
    categories = Category.objects.annotate(
        published_count=Count('blogs', filter=Q(blogs__status='published'))
    ).order_by('-published_count', 'name')

    return render(request, 'blogs/category_list.html', {
        'categories': categories,
        'total_categories': categories.count(),
    })


def tag_detail_view(request, slug):
    """
    Filtered blog list for a specific tag.
    """
    tag = get_object_or_404(Tag, slug=slug)
    blogs_qs = Blog.objects.filter(
        status='published',
        tags=tag
    ).select_related('author', 'author__profile', 'category').prefetch_related('tags').order_by('-created_date')

    paginator = Paginator(blogs_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blogs/tag_detail.html', {
        'tag': tag,
        'page_obj': page_obj,
        'blogs': page_obj.object_list,
        'total_count': paginator.count,
    })


def blog_detail_view(request, slug):
    """
    Complete reading view for a single blog post.
    Enforces draft visibility: only the original author can preview a draft.
    """
    blog = get_object_or_404(
        Blog.objects.select_related('author', 'author__profile', 'category').prefetch_related('tags'),
        slug=slug
    )

    # Permission check for drafts
    if blog.status == 'draft':
        if not (request.user.is_authenticated and request.user == blog.author):
            raise Http404("This article is either unpublished or does not exist.")

    is_author = (request.user.is_authenticated and request.user == blog.author)

    # Interactions: Comments, Likes, and Bookmarks
    comments = blog.comments.select_related('user', 'user__profile').order_by('-created_date')
    comment_form = CommentForm()

    likes_count = blog.likes.count()
    is_liked = False
    is_bookmarked = False

    if request.user.is_authenticated:
        is_liked = blog.likes.filter(user=request.user).exists()
        is_bookmarked = blog.bookmarks.filter(user=request.user).exists()

    # Related articles in same category
    related_blogs = []
    if blog.category:
        related_blogs = Blog.objects.filter(
            status='published',
            category=blog.category
        ).exclude(pk=blog.pk).select_related('author', 'author__profile')[:3]

    return render(request, 'blogs/blog_detail.html', {
        'blog': blog,
        'is_author': is_author,
        'comments': comments,
        'comment_form': comment_form,
        'likes_count': likes_count,
        'is_liked': is_liked,
        'is_bookmarked': is_bookmarked,
        'related_blogs': related_blogs,
    })


@login_required
def blog_create_view(request):
    """
    Allows an authenticated user to write and publish or draft a new blog post.
    """
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=True, author=request.user)
            messages.success(
                request,
                f"Blog post '{blog.title}' has been successfully {blog.get_status_display().lower()}!"
            )
            return redirect('blogs:blog_detail', slug=blog.slug)
        else:
            messages.error(request, "Please correct the errors in the blog form below.")
    else:
        form = BlogPostForm(initial={'status': 'published'})

    return render(request, 'blogs/blog_form.html', {
        'form': form,
        'is_edit': False,
        'page_title': 'Write a New Blog Post',
    })


@login_required
def blog_update_view(request, slug):
    """
    Allows the blog author to edit their existing blog post.
    Server-level permission check strictly forbids non-authors (raises 403 Forbidden).
    """
    blog = get_object_or_404(Blog, slug=slug)

    # Row-level authorization check
    if blog.author != request.user:
        raise PermissionDenied("You do not have permission to edit someone else's blog post.")

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save(commit=True)
            messages.success(
                request,
                f"Blog post '{blog.title}' was successfully updated!"
            )
            return redirect('blogs:blog_detail', slug=blog.slug)
        else:
            messages.error(request, "Please correct the errors in the blog form below.")
    else:
        form = BlogPostForm(instance=blog)

    return render(request, 'blogs/blog_form.html', {
        'form': form,
        'blog': blog,
        'is_edit': True,
        'page_title': f"Edit: {blog.title}",
    })


@login_required
def blog_delete_view(request, slug):
    """
    Handles confirmation and deletion of a blog post.
    Uses POST method for actual deletion to prevent accidental CSRF/GET deletions.
    Strictly forbids non-authors (raises 403 Forbidden).
    """
    blog = get_object_or_404(Blog, slug=slug)

    # Row-level authorization check
    if blog.author != request.user:
        raise PermissionDenied("You do not have permission to delete someone else's blog post.")

    if request.method == 'POST':
        title = blog.title
        blog.delete()
        messages.success(request, f"Blog post '{title}' has been deleted successfully.")
        return redirect('blogs:my_blogs')

    return render(request, 'blogs/blog_confirm_delete.html', {
        'blog': blog
    })


@login_required
def my_blogs_view(request):
    """
    Author's personal dashboard showing all owned articles, including private drafts.
    Supports filtering by status (all, published, draft) and pagination.
    """
    status_filter = request.GET.get('status', 'all').strip().lower()

    blogs_qs = Blog.objects.filter(author=request.user).select_related('category').prefetch_related('tags')

    if status_filter == 'published':
        blogs_qs = blogs_qs.filter(status='published')
    elif status_filter == 'draft':
        blogs_qs = blogs_qs.filter(status='draft')

    blogs_qs = blogs_qs.order_by('-created_date')

    # Metrics
    total_count = request.user.blogs.count()
    published_count = request.user.blogs.filter(status='published').count()
    draft_count = request.user.blogs.filter(status='draft').count()

    # Pagination: 8 blogs per page
    paginator = Paginator(blogs_qs, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blogs/my_blogs.html', {
        'page_obj': page_obj,
        'blogs': page_obj.object_list,
        'status_filter': status_filter,
        'total_count': total_count,
        'published_count': published_count,
        'draft_count': draft_count,
    })
