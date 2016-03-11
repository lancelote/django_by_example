"""Blog forms"""

from django import forms


class EmailPostForm(forms.Form):
    """Post share form"""

    name = forms.CharField(max_length=25)
    sender = forms.EmailField()
    recipient = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
