from django import forms
from django.core.exceptions import ValidationError
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Form for adding a discussion comment to a blog post.
    """
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Share your constructive thoughts, questions, or feedback...'
        }),
        max_length=2000,
        required=True,
        label=""
    )

    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise ValidationError("Comment cannot be empty.")
        if len(content) < 3:
            raise ValidationError("Comment is too short (minimum 3 characters).")
        return content
