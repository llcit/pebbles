# discussions/forms.py
from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['subject', 'text', 'creator', 'parent_post']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': '100%', 'class': 'form-control content-editor'}),
            'creator': forms.HiddenInput(),
            'parent_post': forms.HiddenInput(),
        }
        labels = { 'text': 'Message Text...'}


class PostReplyForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['subject', 'text', 'creator', 'parent_post']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': '100%', 'class': 'form-control discussion-editor'}),
            'subject': forms.HiddenInput(),
            'creator': forms.HiddenInput(),
            'parent_post': forms.HiddenInput(),
        }
        labels = { 'text': ''}