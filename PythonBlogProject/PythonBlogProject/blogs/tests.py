from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from .models import Category, Tag, Blog


class BlogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='blogger1',
            email='blogger1@example.com',
            password='ComplexPassword123!'
        )
        self.category = Category.objects.create(
            name='Web Development',
            description='Articles about modern web tech'
        )
        self.tag = Tag.objects.create(name='Django')

    def test_category_creation_and_slug(self):
        """Test category creation, automatic slugification and string representation."""
        self.assertEqual(self.category.slug, 'web-development')
        self.assertEqual(str(self.category), 'Web Development')

    def test_tag_creation_and_slug(self):
        """Test tag creation, automatic slugification and string representation."""
        self.assertEqual(self.tag.slug, 'django')
        self.assertEqual(str(self.tag), '#Django')

    def test_blog_creation_and_auto_slug(self):
        """Test blog creation, slug generation, excerpt extraction and reading time."""
        blog = Blog.objects.create(
            author=self.user,
            title='Getting Started with Django 5',
            content='Django is a high-level Python web framework that encourages rapid development. ' * 50,
            category=self.category,
            status='published'
        )
        blog.tags.add(self.tag)

        self.assertEqual(blog.slug, 'getting-started-with-django-5')
        self.assertEqual(str(blog), 'Getting Started with Django 5')
        self.assertTrue(blog.excerpt.startswith('Django is a high-level'))
        self.assertGreater(blog.reading_time_minutes, 0)
        self.assertIn(self.tag, blog.tags.all())

    def test_duplicate_blog_slug_deduplication(self):
        """Test that identical blog titles receive distinct slugs."""
        blog1 = Blog.objects.create(
            author=self.user,
            title='Unique Title Exploration',
            content='Some test content here.'
        )
        blog2 = Blog.objects.create(
            author=self.user,
            title='Unique Title Exploration',
            content='Different content here.'
        )

        self.assertEqual(blog1.slug, 'unique-title-exploration')
        self.assertEqual(blog2.slug, 'unique-title-exploration-1')


class BlogCRUDPermissionsAndVisibilityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(
            username='main_author',
            email='main@example.com',
            password='Password123!'
        )
        self.other_user = User.objects.create_user(
            username='other_user',
            email='other@example.com',
            password='Password123!'
        )
        self.category = Category.objects.create(name='Tutorials')

        # Published post
        self.published_blog = Blog.objects.create(
            author=self.author,
            title='Publicly Published Post',
            content='This post is publicly accessible to everyone in the community.',
            category=self.category,
            status='published'
        )

        # Draft post
        self.draft_blog = Blog.objects.create(
            author=self.author,
            title='Private Unpublished Draft',
            content='This post is a work in progress and should be private to author.',
            category=self.category,
            status='draft'
        )

    def test_unauthenticated_cannot_access_create(self):
        """Anonymous user trying to access blog create is redirected to login."""
        response = self.client.get(reverse('blogs:blog_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)

    def test_authenticated_can_create_published_blog(self):
        """Logged-in author creates a published blog post with tags."""
        self.client.force_login(self.author)
        data = {
            'title': 'New Scalable Architecture Blog',
            'excerpt': 'A comprehensive summary of scalable systems.',
            'content': 'Detailed guide describing architectural patterns in modern distributed systems.',
            'category': self.category.id,
            'status': 'published',
            'tags_input': 'python, architecture, cloud'
        }
        response = self.client.post(reverse('blogs:blog_create'), data)
        self.assertEqual(response.status_code, 302)

        new_blog = Blog.objects.get(title='New Scalable Architecture Blog')
        self.assertEqual(new_blog.author, self.author)
        self.assertEqual(new_blog.status, 'published')
        self.assertEqual(new_blog.tags.count(), 3)
        self.assertTrue(Tag.objects.filter(name='architecture').exists())

    def test_authenticated_can_create_draft_blog(self):
        """Logged-in author can save an article as draft."""
        self.client.force_login(self.author)
        data = {
            'title': 'Secret Project in Draft Stage',
            'content': 'Early thoughts on a new experimental project concept.',
            'status': 'draft',
        }
        response = self.client.post(reverse('blogs:blog_create'), data)
        self.assertEqual(response.status_code, 302)

        draft = Blog.objects.get(title='Secret Project in Draft Stage')
        self.assertEqual(draft.status, 'draft')
        self.assertEqual(draft.author, self.author)

    def test_public_can_read_published_blog(self):
        """Anonymous visitor can read published blogs."""
        response = self.client.get(
            reverse('blogs:blog_detail', kwargs={'slug': self.published_blog.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Publicly Published Post')
        self.assertContains(response, 'main_author')

    def test_author_can_view_own_draft(self):
        """Author can preview their own draft post."""
        self.client.force_login(self.author)
        response = self.client.get(
            reverse('blogs:blog_detail', kwargs={'slug': self.draft_blog.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Private Unpublished Draft')
        self.assertContains(response, 'Private Draft Preview')

    def test_other_user_cannot_view_draft(self):
        """Other users receive 404 when trying to view someone else's draft."""
        self.client.force_login(self.other_user)
        response = self.client.get(
            reverse('blogs:blog_detail', kwargs={'slug': self.draft_blog.slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_anonymous_cannot_view_draft(self):
        """Anonymous visitor receives 404 when trying to view a draft."""
        response = self.client.get(
            reverse('blogs:blog_detail', kwargs={'slug': self.draft_blog.slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_draft_not_visible_in_public_feed(self):
        """Draft posts must not appear in the public blog listing."""
        response = self.client.get(reverse('blogs:blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Publicly Published Post')
        self.assertNotContains(response, 'Private Unpublished Draft')

    def test_author_can_update_own_blog(self):
        """Author can update their existing blog post."""
        self.client.force_login(self.author)
        data = {
            'title': 'Publicly Published Post - Updated Version',
            'excerpt': self.published_blog.excerpt,
            'content': 'Updated content with fresh examples and deeper technical explanations.',
            'category': self.category.id,
            'status': 'published',
            'tags_input': 'updated, django'
        }
        response = self.client.post(
            reverse('blogs:blog_update', kwargs={'slug': self.published_blog.slug}),
            data
        )
        self.assertEqual(response.status_code, 302)

        self.published_blog.refresh_from_db()
        self.assertEqual(self.published_blog.title, 'Publicly Published Post - Updated Version')
        self.assertIn('Updated content with fresh examples', self.published_blog.content)

    def test_unauthorized_user_cannot_update_blog(self):
        """User B attempting to edit User A's blog receives 403 Forbidden."""
        self.client.force_login(self.other_user)
        # GET attempt
        response_get = self.client.get(
            reverse('blogs:blog_update', kwargs={'slug': self.published_blog.slug})
        )
        self.assertEqual(response_get.status_code, 403)

        # POST attempt
        data = {
            'title': 'Hacked Title Attempt',
            'content': 'Malicious modification attempt.',
            'status': 'published'
        }
        response_post = self.client.post(
            reverse('blogs:blog_update', kwargs={'slug': self.published_blog.slug}),
            data
        )
        self.assertEqual(response_post.status_code, 403)

        # Confirm post unchanged
        self.published_blog.refresh_from_db()
        self.assertNotEqual(self.published_blog.title, 'Hacked Title Attempt')

    def test_unauthorized_user_cannot_delete_blog(self):
        """User B attempting to delete User A's blog receives 403 Forbidden."""
        self.client.force_login(self.other_user)
        response = self.client.post(
            reverse('blogs:blog_delete', kwargs={'slug': self.published_blog.slug})
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Blog.objects.filter(pk=self.published_blog.pk).exists())

    def test_author_can_delete_own_blog(self):
        """Author can delete their own blog post via POST confirmation."""
        self.client.force_login(self.author)
        response = self.client.post(
            reverse('blogs:blog_delete', kwargs={'slug': self.published_blog.slug})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Blog.objects.filter(pk=self.published_blog.pk).exists())

    def test_my_blogs_dashboard_shows_all_own_posts(self):
        """Author dashboard displays their own drafts and published posts."""
        self.client.force_login(self.author)
        response = self.client.get(reverse('blogs:my_blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Publicly Published Post')
        self.assertContains(response, 'Private Unpublished Draft')

        # Test filtering by draft
        response_drafts = self.client.get(reverse('blogs:my_blogs') + '?status=draft')
        self.assertEqual(response_drafts.status_code, 200)
        self.assertContains(response_drafts, 'Private Unpublished Draft')
        self.assertNotContains(response_drafts, 'Publicly Published Post')

    def test_pagination_on_blog_list(self):
        """Verify pagination divides posts into pages of 6."""
        # Create 7 additional published blogs (total 8 published)
        for i in range(7):
            Blog.objects.create(
                author=self.author,
                title=f'Pagination Test Article {i}',
                content='Test content for pagination checking.',
                status='published'
            )

        # Page 1 should contain 6 blogs and have next page
        response_p1 = self.client.get(reverse('blogs:blog_list'))
        self.assertEqual(response_p1.status_code, 200)
        self.assertEqual(len(response_p1.context['blogs']), 6)
        self.assertTrue(response_p1.context['page_obj'].has_next())

        # Page 2 should contain 2 blogs and not have next page
        response_p2 = self.client.get(reverse('blogs:blog_list') + '?page=2')
        self.assertEqual(response_p2.status_code, 200)
        self.assertEqual(len(response_p2.context['blogs']), 2)
        self.assertFalse(response_p2.context['page_obj'].has_next())


class PublicDiscoveryFeaturesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(
            username='techwriter',
            email='tech@example.com',
            password='Password123!'
        )
        self.author.profile.bio = 'Python Architect & Cloud Consultant'
        self.author.profile.skills = 'Python, Django, AWS, Kubernetes'
        self.author.profile.interests = 'Cloud Computing, Microservices'
        self.author.profile.save()

        self.category_py = Category.objects.create(
            name='Python Core',
            description='Deep dive into Python language features.'
        )
        self.category_web = Category.objects.create(
            name='Web Engineering',
            description='Modern web architecture guides.'
        )

        self.tag_django = Tag.objects.create(name='Django')
        self.tag_orm = Tag.objects.create(name='ORM')

        # Published post
        self.pub_blog = Blog.objects.create(
            author=self.author,
            title='Mastering Django ORM Optimization',
            excerpt='Learn how to optimize Django queries and eliminate N+1 issues.',
            content='Comprehensive exploration of select_related and prefetch_related for high performance.',
            category=self.category_py,
            status='published'
        )
        self.pub_blog.tags.add(self.tag_django, self.tag_orm)

        # Draft post
        self.draft_blog = Blog.objects.create(
            author=self.author,
            title='Unreleased Internal Draft on Microservices',
            excerpt='Secret excerpt for internal draft.',
            content='Unpublished confidential design document.',
            category=self.category_web,
            status='draft'
        )

    def test_home_page_displays_recent_published_and_excludes_drafts(self):
        """Home page displays recent published blogs and never drafts."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mastering Django ORM Optimization')
        self.assertNotContains(response, 'Unreleased Internal Draft on Microservices')
        self.assertContains(response, 'Python Core')
        self.assertContains(response, 'techwriter')

    def test_categories_page_lists_categories(self):
        """Categories page displays categories with descriptions and counts."""
        response = self.client.get(reverse('blogs:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Core')
        self.assertContains(response, 'Web Engineering')
        self.assertContains(response, '1 article')

    def test_tag_detail_page_filters_by_tag(self):
        """Tag detail page shows articles associated with the requested tag."""
        response = self.client.get(
            reverse('blogs:tag_detail', kwargs={'slug': 'django'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mastering Django ORM Optimization')
        self.assertContains(response, '#Django')

    def test_global_search_finds_matching_blog(self):
        """Global search finds published blogs by title, excerpt, and content."""
        response = self.client.get(reverse('search') + '?q=Optimization&tab=blogs')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mastering Django ORM Optimization')
        # Drafts must NOT appear in search
        self.assertNotContains(response, 'Unreleased Internal Draft on Microservices')

    def test_global_search_excludes_drafts_even_when_query_matches(self):
        """Searching specifically for a draft keyword returns empty state."""
        response = self.client.get(reverse('search') + '?q=Microservices&tab=blogs')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Unreleased Internal Draft on Microservices')
        self.assertContains(response, 'No Articles Found')

    def test_global_search_finds_authors_by_skill_and_bio(self):
        """Global search finds authors by skills, bio, or username."""
        response = self.client.get(reverse('search') + '?q=Kubernetes&tab=authors')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'techwriter')
        self.assertContains(response, 'Python Architect')

    def test_global_search_empty_state_when_no_match(self):
        """Search displays friendly empty state when no records match."""
        response = self.client.get(reverse('search') + '?q=nonexistentkeyword123')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No Articles Found')

    def test_explore_page_sorting_newest_first(self):
        """Explore blogs page orders published articles by newest first."""
        from datetime import timedelta
        from django.utils import timezone

        # Ensure older blog has an explicitly earlier timestamp to prevent sub-millisecond tie
        Blog.objects.filter(pk=self.pub_blog.pk).update(
            created_date=timezone.now() - timedelta(days=2)
        )

        second_blog = Blog.objects.create(
            author=self.author,
            title='Brand New Second Article',
            content='Testing order of arrival in published stream.',
            status='published'
        )
        response = self.client.get(reverse('blogs:blog_list'))
        self.assertEqual(response.status_code, 200)
        blogs = list(response.context['blogs'])
        # Newest blog must appear before older blog
        self.assertEqual(blogs[0].pk, second_blog.pk)
        self.assertEqual(blogs[1].pk, self.pub_blog.pk)

