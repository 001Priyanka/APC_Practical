from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Count, Q

from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from blogs.models import Blog


def register_view(request):
    """
    Handles new user account registration.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate and login the new user automatically
            login(request, user)
            messages.success(
                request,
                f"Welcome to BlogHub, {user.username}! Your account has been created."
            )
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below to register.")
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Handles user authentication and login with redirect validation.
    """
    if request.user.is_authenticated:
        return redirect('home')

    redirect_to = request.POST.get('next') or request.GET.get('next') or ''

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")

            # Validate redirect URL to prevent open-redirect vulnerabilities
            if redirect_to and url_has_allowed_host_and_scheme(
                url=redirect_to,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure()
            ):
                return redirect(redirect_to)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {
        'form': form,
        'next': redirect_to
    })


def logout_view(request):
    """
    Handles secure logout (requires POST or handles GET safely).
    """
    if request.method == 'POST' or request.user.is_authenticated:
        logout(request)
        messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def profile_edit_view(request):
    """
    Allows an authenticated user to update their own profile and personal details.
    Row-level security: only request.user's own records can be edited.
    """
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('accounts:profile_detail', username=user.username)
        else:
            messages.error(request, "Please correct the form errors below.")
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def profile_detail_view(request, username):
    """
    Public author portfolio page.
    Displays author bio, verified skills, interests, and all published blogs.
    Private information (email) is hidden from other visitors.
    """
    author = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=author)

    # Fetch only published blogs for public view
    published_blogs = Blog.objects.filter(
        author=author,
        status='published'
    ).select_related('category').prefetch_related('tags').order_by('-created_date')

    is_owner = (request.user.is_authenticated and request.user == author)
    draft_count = 0
    if is_owner:
        draft_count = Blog.objects.filter(author=author, status='draft').count()

    return render(request, 'accounts/profile_detail.html', {
        'author': author,
        'profile': profile,
        'blogs': published_blogs,
        'is_owner': is_owner,
        'draft_count': draft_count,
        'skills_list': profile.get_skills_list(),
        'interests_list': profile.get_interests_list(),
    })


def author_list_view(request):
    """
    Public directory of authors on BlogHub.
    Allows filtering by skill or search query.
    """
    search_query = request.GET.get('q', '').strip()
    skill_filter = request.GET.get('skill', '').strip()

    authors_qs = User.objects.filter(is_active=True).select_related('profile').annotate(
        published_blogs_count=Count(
            'blogs',
            filter=Q(blogs__status='published')
        )
    ).order_by('-published_blogs_count', 'username')

    if search_query:
        authors_qs = authors_qs.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(profile__skills__icontains=search_query) |
            Q(profile__bio__icontains=search_query)
        )

    if skill_filter:
        authors_qs = authors_qs.filter(profile__skills__icontains=skill_filter)

    return render(request, 'accounts/author_list.html', {
        'authors': authors_qs,
        'search_query': search_query,
        'skill_filter': skill_filter,
    })
