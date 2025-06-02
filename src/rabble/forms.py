from django import forms
from .models import Post, Comment, SubRabble, User

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
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Members"
    )

    class Meta:
        model = SubRabble
        fields = [
            'subrabble_community_id',
            'subrabble_name',
            'description',
            'allow_anonymous',
            'private',
            'members',
        ]
        widgets = {
            'subrabble_community_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter community ID (no spaces allowed)…',
                'pattern': '[^\\s]*',
                'title': 'Community ID cannot contain spaces'
            }),
            'subrabble_name':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter sub-Rabble name…'}),
            'description':         forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'What is this sub-Rabble about?'}),
            'allow_anonymous':     forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'private':             forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'subrabble_community_id': 'Community ID',
            'subrabble_name':         'Name',
            'description':            'Description',
            'allow_anonymous':        'Allow anonymous posts?',
            'private':                'Private sub-Rabble?',
            'members':                'Members',
        }

    def clean_subrabble_community_id(self):
        community_id = self.cleaned_data.get('subrabble_community_id')
        if ' ' in community_id:
            raise forms.ValidationError("Community ID cannot contain spaces.")
        return community_id

    def __init__(self, *args, rabble=None, **kwargs):
        super().__init__(*args, **kwargs)
        if rabble:
            self.fields['members'].queryset = rabble.members.all()
        else:
            self.fields['members'].queryset = User.objects.none()