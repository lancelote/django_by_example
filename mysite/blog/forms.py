# pylint: disable=too-few-public-methods, missing-docstring

"""Blog forms"""

from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    """Post share form"""

    name = forms.CharField(max_length=25)
    sender = forms.EmailField()
    recipient = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    """New comment form for post detail page"""

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
