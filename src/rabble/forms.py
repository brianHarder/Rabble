from django import forms
from .models import Post, Comment, SubRabble

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'anonymous']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Write your title here…',
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your post here…',
            }),
            'anonymous': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'title': 'Title',
            'body': 'Body',
            'anonymous': 'Post anonymously',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'anonymous']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your comment here…',
            }),
            'anonymous': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'text': 'Text',
            'anonymous': 'Post anonymously',
        }

class SubRabbleForm(forms.ModelForm):
    class Meta:
        model = SubRabble
        fields = [
            'subrabble_community_id',
            'subrabble_name',
            'description',
            'allow_anonymous',
            'private',
        ]
        widgets = {
            'subrabble_community_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter unique community ID…',
            }),
            'subrabble_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter sub-Rabble name…',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'What is this sub-Rabble about?',
            }),
            'allow_anonymous': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'private': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'subrabble_community_id': 'Community ID',
            'subrabble_name': 'Name',
            'description': 'Description',
            'allow_anonymous': 'Allow anonymous posts?',
            'private': 'Private sub-Rabble?',
        }
