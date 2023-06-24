from django import forms
from .models import Comment


MAX_NAME_LENGTH = 25


class EmailPostForm(forms.Form):
    """Форма для отправки поста по email."""
    name = forms.CharField(max_length=MAX_NAME_LENGTH)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentPostForm(forms.ModelForm):
    """Форма для добавления комментария к посту."""
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
