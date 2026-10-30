from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .models import Blog, Category, Tag
from config.validators import validate_cover_image


class BlogPostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts.
    Allows managing title, excerpt, content, cover image, category, status, and tags.
    """
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter an engaging blog title...'
        }),
        help_text="Titles should be descriptive and clear."
    )
    excerpt = forms.CharField(
        max_length=350,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Provide a brief summary (optional - auto-generated from content if left blank)...'
        }),
        help_text="Shown in article cards and search results."
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 14,
            'placeholder': 'Write your blog post content here...'
        }),
        help_text="Share your complete story, insights, code, or guide."
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select a Category (Optional)",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=Blog.STATUS_CHOICES,
        initial='draft',
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Choose 'Draft' to keep working privately or 'Published' to make it live."
    )
    tags_input = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. python, django, tutorial, tips'
        }),
        help_text="Enter tags separated by commas. Existing or new tags will be applied automatically."
    )

    class Meta:
        model = Blog
        fields = ['title', 'excerpt', 'content', 'cover_image', 'category', 'status']
        widgets = {
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prepopulate tags_input when editing an existing blog instance
        if self.instance and self.instance.pk:
            self.fields['tags_input'].initial = ", ".join(
                self.instance.tags.values_list('name', flat=True)
            )

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 5:
            raise ValidationError("Blog title must be at least 5 characters long.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if len(content) < 20:
            raise ValidationError("Blog content must contain at least 20 characters.")
        return content

    def clean_cover_image(self):
        image = self.cleaned_data.get('cover_image')
        if image and hasattr(image, 'file'):
            validate_cover_image(image)
        return image

    def save(self, commit=True, author=None):
        blog = super().save(commit=False)
        if author and not blog.author_id:
            blog.author = author

        if commit:
            blog.save()
            self.save_m2m()

            # Process comma-separated tags
            tags_str = self.cleaned_data.get('tags_input', '')
            if tags_str is not None:
                tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
                tag_objects = []
                for name in tag_names:
                    tag_obj, _ = Tag.objects.get_or_create(
                        name__iexact=name,
                        defaults={'name': name, 'slug': slugify(name)}
                    )
                    tag_objects.append(tag_obj)
                blog.tags.set(tag_objects)

        return blog
