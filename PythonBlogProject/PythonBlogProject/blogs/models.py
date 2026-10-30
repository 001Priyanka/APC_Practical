import math
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from config.validators import validate_cover_image


class Category(models.Model):
    """
    Editorial category for organizing blogs (e.g., Python, Tutorials, Career).
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, help_text="Brief description of the category.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """
    Keyword tags associated with blogs for discovery.
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="Tag Name")
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['name']

    def __str__(self):
        return f"#{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Blog(models.Model):
    """
    Core blog post entity authored by a User.
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blogs',
        verbose_name="Author"
    )
    title = models.CharField(max_length=200, verbose_name="Blog Title")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    excerpt = models.CharField(
        max_length=350,
        blank=True,
        help_text="Short excerpt or summary for search results and cards."
    )
    content = models.TextField(help_text="Full blog post content.")
    cover_image = models.ImageField(
        upload_to='blogs/covers/',
        blank=True,
        null=True,
        validators=[validate_cover_image],
        help_text="Cover header image (JPG, PNG, WEBP up to 5MB)."
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blogs',
        verbose_name="Category"
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='blogs',
        blank=True,
        verbose_name="Tags"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        db_index=True
    )
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-created_date', '-id']
        indexes = [
            models.Index(fields=['status', '-created_date'], name='blog_status_created_idx'),
            models.Index(fields=['slug'], name='blog_slug_idx'),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "blog"
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        if not self.excerpt and self.content:
            # Auto-generate excerpt if empty
            plain_text = self.content.strip()
            self.excerpt = plain_text[:280] + ("..." if len(plain_text) > 280 else "")

        super().save(*args, **kwargs)

    @property
    def reading_time_minutes(self):
        """Estimate reading time in minutes (~200 words per minute)."""
        words = len(self.content.split())
        return max(1, math.ceil(words / 200))
