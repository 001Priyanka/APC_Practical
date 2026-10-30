from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse
from blogs.models import Blog
from .models import Comment, Like, Bookmark


class InteractionModelsTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='blog_author',
            email='author@example.com',
            password='Password123!'
        )
        self.reader = User.objects.create_user(
            username='blog_reader',
            email='reader@example.com',
            password='Password123!'
        )
        self.blog = Blog.objects.create(
            author=self.author,
            title='Interactive Features in BlogHub',
            content='Discussing comments, likes, and bookmarks.',
            status='published'
        )

    def test_comment_creation_and_str(self):
        """Test comment creation and string representation."""
        comment = Comment.objects.create(
            blog=self.blog,
            user=self.reader,
            content='Great article! Really enjoyed reading it.'
        )
        self.assertEqual(
            str(comment),
            f"Comment by {self.reader.username} on '{self.blog.title}'"
        )
        self.assertEqual(comment.blog, self.blog)
        self.assertEqual(comment.user, self.reader)

    def test_like_creation_and_unique_constraint(self):
        """Test like creation and enforce one like per user per blog."""
        like = Like.objects.create(
            blog=self.blog,
            user=self.reader
        )
        self.assertEqual(str(like), f"{self.reader.username} likes '{self.blog.title}'")

        # Second like by same user on same blog must raise IntegrityError
        with self.assertRaises(IntegrityError):
            Like.objects.create(
                blog=self.blog,
                user=self.reader
            )

    def test_bookmark_creation_and_unique_constraint(self):
        """Test bookmark creation and enforce one bookmark per user per blog."""
        bookmark = Bookmark.objects.create(
            blog=self.blog,
            user=self.reader
        )
        self.assertEqual(str(bookmark), f"{self.reader.username} bookmarked '{self.blog.title}'")

        # Second bookmark by same user on same blog must raise IntegrityError
        with self.assertRaises(IntegrityError):
            Bookmark.objects.create(
                blog=self.blog,
                user=self.reader
            )


class InteractionViewsAndPermissionsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(
            username='author_user',
            email='author@example.com',
            password='Password123!'
        )
        self.commenter = User.objects.create_user(
            username='commenter_user',
            email='commenter@example.com',
            password='Password123!'
        )
        self.unrelated_user = User.objects.create_user(
            username='unrelated_user',
            email='unrelated@example.com',
            password='Password123!'
        )
        self.blog = Blog.objects.create(
            author=self.author,
            title='Real World Discussion Article',
            content='Detailed tutorial encouraging user commentary and feedback.',
            status='published'
        )

    def test_authenticated_can_post_comment(self):
        """Authenticated user posts a comment on a published blog."""
        self.client.force_login(self.commenter)
        response = self.client.post(
            reverse('interactions:add_comment', kwargs={'blog_id': self.blog.id}),
            {'content': 'This is a genuinely insightful guide. Thank you!'}
        )
        self.assertEqual(response.status_code, 302)

        comment = Comment.objects.get(blog=self.blog)
        self.assertEqual(comment.user, self.commenter)
        self.assertEqual(comment.content, 'This is a genuinely insightful guide. Thank you!')

    def test_unauthenticated_cannot_post_comment(self):
        """Anonymous user is redirected to login when trying to comment."""
        response = self.client.post(
            reverse('interactions:add_comment', kwargs={'blog_id': self.blog.id}),
            {'content': 'Anonymous comment attempt.'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)
        self.assertFalse(Comment.objects.filter(blog=self.blog).exists())

    def test_empty_comment_rejected(self):
        """Posting an empty or whitespace comment is rejected."""
        self.client.force_login(self.commenter)
        response = self.client.post(
            reverse('interactions:add_comment', kwargs={'blog_id': self.blog.id}),
            {'content': '   '}
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(blog=self.blog).exists())

    def test_commenter_can_delete_own_comment(self):
        """The comment author can delete their own comment via POST."""
        comment = Comment.objects.create(
            blog=self.blog,
            user=self.commenter,
            content='I want to remove this comment later.'
        )
        self.client.force_login(self.commenter)
        response = self.client.post(
            reverse('interactions:delete_comment', kwargs={'comment_id': comment.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

    def test_blog_author_can_delete_comments_on_their_blog(self):
        """The blog owner can moderate/delete any comment on their blog."""
        comment = Comment.objects.create(
            blog=self.blog,
            user=self.commenter,
            content='Spam or inappropriate remark.'
        )
        self.client.force_login(self.author)
        response = self.client.post(
            reverse('interactions:delete_comment', kwargs={'comment_id': comment.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

    def test_unauthorized_user_cannot_delete_other_user_comment(self):
        """Unrelated user attempting to delete another user's comment receives 403 Forbidden."""
        comment = Comment.objects.create(
            blog=self.blog,
            user=self.commenter,
            content='Valid community comment.'
        )
        self.client.force_login(self.unrelated_user)
        response = self.client.post(
            reverse('interactions:delete_comment', kwargs={'comment_id': comment.id})
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Comment.objects.filter(pk=comment.pk).exists())

    def test_toggle_like_behavior(self):
        """Like reaction toggles on first click and removes on second click."""
        self.client.force_login(self.commenter)
        like_url = reverse('interactions:toggle_like', kwargs={'blog_id': self.blog.id})

        # First click: like added
        response1 = self.client.post(like_url)
        self.assertEqual(response1.status_code, 302)
        self.assertTrue(Like.objects.filter(blog=self.blog, user=self.commenter).exists())
        self.assertEqual(self.blog.likes.count(), 1)

        # Second click: like removed
        response2 = self.client.post(like_url)
        self.assertEqual(response2.status_code, 302)
        self.assertFalse(Like.objects.filter(blog=self.blog, user=self.commenter).exists())
        self.assertEqual(self.blog.likes.count(), 0)

    def test_toggle_bookmark_and_saved_bookmarks_list(self):
        """Bookmark toggles and renders on user's saved bookmarks page."""
        self.client.force_login(self.commenter)
        bookmark_url = reverse('interactions:toggle_bookmark', kwargs={'blog_id': self.blog.id})

        # Bookmark post
        response1 = self.client.post(bookmark_url)
        self.assertEqual(response1.status_code, 302)
        self.assertTrue(Bookmark.objects.filter(blog=self.blog, user=self.commenter).exists())

        # View saved bookmarks page
        response_list = self.client.get(reverse('interactions:bookmarks_list'))
        self.assertEqual(response_list.status_code, 200)
        self.assertContains(response_list, 'Real World Discussion Article')

        # Other user's bookmarks page does NOT show commenter's bookmark
        self.client.force_login(self.unrelated_user)
        response_unrelated = self.client.get(reverse('interactions:bookmarks_list'))
        self.assertEqual(response_unrelated.status_code, 200)
        self.assertNotContains(response_unrelated, 'Real World Discussion Article')
        self.assertContains(response_unrelated, 'No Bookmarks Saved')
