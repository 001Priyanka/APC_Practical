from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile
from blogs.models import Blog, Category


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testauthor',
            email='author@example.com',
            password='ComplexPassword123!'
        )

    def test_profile_auto_created_by_signal(self):
        """Verify that creating a User automatically generates a matching Profile."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)

    def test_profile_str_representation(self):
        """Verify the Profile string method."""
        self.assertEqual(str(self.user.profile), "testauthor's Profile")

    def test_skills_and_interests_helpers(self):
        """Verify skills and interests list parsing."""
        profile = self.user.profile
        profile.skills = "Python, Django, MySQL, Docker"
        profile.interests = "Web Development, Machine Learning"
        profile.save()

        self.assertEqual(profile.get_skills_list(), ['Python', 'Django', 'MySQL', 'Docker'])
        self.assertEqual(profile.get_interests_list(), ['Web Development', 'Machine Learning'])


class RegistrationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.existing_user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='ExistingPassword123!'
        )

    def test_registration_page_renders(self):
        """Verify registration page loads with HTTP 200."""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_valid_registration(self):
        """Verify successful user registration and auto-login."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!'
        }
        response = self.client.post(reverse('accounts:register'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # Verify profile auto-created
        new_user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(new_user, 'profile'))
        self.assertEqual(new_user.first_name, 'Jane')

        # Verify user is logged in
        self.assertEqual(int(self.client.session['_auth_user_id']), new_user.pk)

    def test_duplicate_username_rejected(self):
        """Verify registration rejects duplicate username with friendly error."""
        data = {
            'username': 'existinguser',
            'email': 'different@example.com',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!'
        }
        response = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            'username',
            'A user with that username already exists.'
        )

    def test_duplicate_email_rejected(self):
        """Verify registration rejects duplicate email."""
        data = {
            'username': 'uniqueuser',
            'email': 'existing@example.com',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!'
        }
        response = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            'email',
            'A user with this email address is already registered.'
        )

    def test_password_mismatch_rejected(self):
        """Verify password and confirm password must match."""
        data = {
            'username': 'uniqueuser2',
            'email': 'unique2@example.com',
            'password': 'StrongPassword123!',
            'confirm_password': 'DifferentPassword123!'
        }
        response = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            'confirm_password',
            'Passwords do not match.'
        )

    def test_authenticated_user_redirected_from_register(self):
        """Authenticated user should be redirected away from register page."""
        self.client.force_login(self.existing_user)
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 302)


class LoginLogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = 'SecretPassword123!'
        self.user = User.objects.create_user(
            username='loginuser',
            email='login@example.com',
            password=self.password
        )

    def test_login_page_renders(self):
        """Verify login page loads with HTTP 200."""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_valid_login(self):
        """Verify successful user authentication."""
        data = {
            'username': 'loginuser',
            'password': self.password
        }
        response = self.client.post(reverse('accounts:login'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_invalid_login_wrong_password(self):
        """Verify login fails with wrong password."""
        data = {
            'username': 'loginuser',
            'password': 'WrongPassword999!'
        }
        response = self.client.post(reverse('accounts:login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_invalid_login_nonexistent_user(self):
        """Verify login fails with non-existent username."""
        data = {
            'username': 'nonexistent',
            'password': 'AnyPassword123!'
        }
        response = self.client.post(reverse('accounts:login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_successful_logout(self):
        """Verify user logout clears session."""
        self.client.force_login(self.user)
        response = self.client.post(reverse('accounts:logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)


class ProfileEditAndSecurityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='author1',
            email='author1@example.com',
            password='Password123!'
        )
        self.other_user = User.objects.create_user(
            username='author2',
            email='author2@example.com',
            password='Password123!'
        )

    def test_unauthenticated_profile_edit_redirects(self):
        """Anonymous user trying to access profile edit is redirected to login."""
        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)

    def test_valid_profile_update(self):
        """Logged-in user can update their bio, skills, and names."""
        self.client.force_login(self.user)
        data = {
            'first_name': 'UpdatedFirst',
            'last_name': 'UpdatedLast',
            'email': 'author1_updated@example.com',
            'bio': 'Senior Django Engineer & Cloud Enthusiast',
            'skills': 'Python, Django, MySQL, AWS',
            'interests': 'Distributed Systems, High Availability'
        }
        response = self.client.post(reverse('accounts:profile_edit'), data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Refresh from database
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'UpdatedFirst')
        self.assertEqual(self.user.email, 'author1_updated@example.com')
        self.assertEqual(self.user.profile.bio, 'Senior Django Engineer & Cloud Enthusiast')
        self.assertEqual(self.user.profile.skills, 'Python, Django, MySQL, AWS')

    def test_duplicate_email_on_profile_update_rejected(self):
        """User cannot change their email to an email used by another user."""
        self.client.force_login(self.user)
        data = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': 'author2@example.com',  # already taken by other_user
            'bio': 'Some bio'
        }
        response = self.client.post(reverse('accounts:profile_edit'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['user_form'],
            'email',
            'This email is already in use by another account.'
        )


class PublicProfileAndAuthorDiscoveryTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(
            username='proauthor',
            email='pro@example.com',
            password='Password123!'
        )
        self.author.profile.bio = 'Specialist in Backend Systems'
        self.author.profile.skills = 'Python, Django, PostgreSQL'
        self.author.profile.save()

        self.category = Category.objects.create(name='Tutorials')

        # Create published blog
        self.published_blog = Blog.objects.create(
            author=self.author,
            title='Building High-Performance APIs',
            content='Step by step guide to fast APIs.',
            category=self.category,
            status='published'
        )

        # Create draft blog
        self.draft_blog = Blog.objects.create(
            author=self.author,
            title='Secret Unpublished Draft',
            content='Work in progress.',
            category=self.category,
            status='draft'
        )

    def test_public_profile_shows_published_blogs(self):
        """Public profile displays author info and published blogs."""
        response = self.client.get(
            reverse('accounts:profile_detail', kwargs={'username': 'proauthor'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Building High-Performance APIs')
        self.assertContains(response, 'Specialist in Backend Systems')
        # Draft blogs must NOT appear on public author page for other visitors
        self.assertNotContains(response, 'Secret Unpublished Draft')

    def test_author_list_view_and_filtering(self):
        """Author directory renders and filters by skill query."""
        response = self.client.get(reverse('accounts:author_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'proauthor')

        # Filter by matching skill
        response_filtered = self.client.get(
            reverse('accounts:author_list') + '?skill=Python'
        )
        self.assertEqual(response_filtered.status_code, 200)
        self.assertContains(response_filtered, 'proauthor')

        # Filter by non-matching skill
        response_non_match = self.client.get(
            reverse('accounts:author_list') + '?skill=Rust'
        )
        self.assertEqual(response_non_match.status_code, 200)
        self.assertNotContains(response_non_match, '@proauthor')
