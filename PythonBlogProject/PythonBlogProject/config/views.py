from django.shortcuts import render
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from blogs.models import Blog, Category, Tag


def home(request):
    """
    Renders the platform homepage featuring recent published blogs,
    active categories, and an author spotlight based on real database activity.
    """
    recent_blogs = Blog.objects.filter(
        status='published'
    ).select_related('author', 'author__profile', 'category').prefetch_related('tags').order_by('-created_date')[:6]

    # Active categories with published blogs count
    featured_categories = Category.objects.annotate(
        published_count=Count('blogs', filter=Q(blogs__status='published'))
    ).filter(published_count__gt=0).order_by('-published_count', 'name')[:6]

    # Authors with at least one published blog
    active_authors = User.objects.filter(
        is_active=True
    ).select_related('profile').annotate(
        published_count=Count('blogs', filter=Q(blogs__status='published'))
    ).filter(published_count__gt=0).order_by('-published_count', 'username')[:4]

    # Real platform metrics
    total_published_blogs = Blog.objects.filter(status='published').count()
    total_active_authors = User.objects.filter(
        is_active=True,
        blogs__status='published'
    ).distinct().count()

    return render(request, 'home.html', {
        'recent_blogs': recent_blogs,
        'featured_categories': featured_categories,
        'active_authors': active_authors,
        'total_published_blogs': total_published_blogs,
        'total_active_authors': total_active_authors,
    })


def global_search_view(request):
    """
    Unified multi-entity search across published blogs and author profiles.
    """
    search_query = request.GET.get('q', '').strip()
    active_tab = request.GET.get('tab', 'blogs')

    matching_blogs = []
    matching_authors = []
    blogs_page_obj = None

    if search_query:
        # Search blogs: title, excerpt, content, tags
        blogs_qs = Blog.objects.filter(
            status='published'
        ).filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        ).select_related('author', 'author__profile', 'category').prefetch_related('tags').distinct().order_by('-created_date')

        # Pagination for blog search results (6 per page)
        paginator = Paginator(blogs_qs, 6)
        page_number = request.GET.get('page')
        blogs_page_obj = paginator.get_page(page_number)
        matching_blogs = blogs_page_obj.object_list

        # Search authors: username, name, bio, skills, interests
        authors_qs = User.objects.filter(
            is_active=True
        ).filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(profile__bio__icontains=search_query) |
            Q(profile__skills__icontains=search_query) |
            Q(profile__interests__icontains=search_query)
        ).select_related('profile').annotate(
            published_blogs_count=Count('blogs', filter=Q(blogs__status='published'))
        ).distinct().order_by('-published_blogs_count', 'username')

        matching_authors = authors_qs

    return render(request, 'search.html', {
        'search_query': search_query,
        'active_tab': active_tab,
        'blogs': matching_blogs,
        'page_obj': blogs_page_obj,
        'authors': matching_authors,
        'blogs_count': blogs_page_obj.paginator.count if blogs_page_obj else 0,
        'authors_count': len(matching_authors) if matching_authors else 0,
    })
