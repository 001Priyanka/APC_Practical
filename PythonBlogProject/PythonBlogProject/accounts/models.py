from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from config.validators import validate_avatar_image


class Profile(models.Model):
    """
    Profile extension for the built-in Django User model.
    Stores bio, profile image, skills, and personal interests.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="User Account"
    )
    bio = models.TextField(
        max_length=1000,
        blank=True,
        help_text="Brief summary about yourself, background, and goals."
    )
    profile_image = models.ImageField(
        upload_to='profiles/avatars/',
        blank=True,
        null=True,
        validators=[validate_avatar_image],
        help_text="Optional profile photo (JPG, PNG, WEBP up to 2MB)."
    )
    skills = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated skills (e.g., Python, Django, MySQL, Docker)."
    )
    interests = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated interests or favorite topics (e.g., AI, Backend, Web Development)."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_skills_list(self):
        """Return skills as a clean list of strings."""
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    def get_interests_list(self):
        """Return interests as a clean list of strings."""
        if not self.interests:
            return []
        return [i.strip() for i in self.interests.split(',') if i.strip()]


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver to automatically create a Profile instance
    whenever a new User is registered.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        # Save profile if it exists
        if hasattr(instance, 'profile'):
            instance.profile.save()
