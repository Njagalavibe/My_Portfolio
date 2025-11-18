
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Only 'content' since we're keeping it simple
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'cols': 50,
                'placeholder': 'Write your comment here...'
            })
        }