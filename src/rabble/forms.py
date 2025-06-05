from django import forms
from .models import Post, Comment, SubRabble, User, Rabble
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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
            # If the rabble is private, only show its members
            # Otherwise show all users
            if rabble.private:
                self.fields['members'].queryset = rabble.members.all()
            else:
                self.fields['members'].queryset = User.objects.all()
            
            # If this is a new subrabble (no instance), set the initial members to include the current user
            if not self.instance.pk:
                self.initial['members'] = [self.current_user.id] if hasattr(self, 'current_user') else []
        else:
            self.fields['members'].queryset = User.objects.none()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'profile_picture']
        labels = {
            'password1': 'Password',
            'password2': 'Confirm Password'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style all fields with Bootstrap classes
        for field_name in ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']:
            placeholder = {
                'password1': 'Enter your password',
                'password2': 'Confirm your password'
            }.get(field_name, f'Enter your {field_name.replace("_", " ").title()}')
            
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control rabble-input',
                'placeholder': placeholder
            })
            # Remove the default label suffix
            self.fields[field_name].label_suffix = ''
            # Set the label class
            if field_name not in ['password1', 'password2']:
                self.fields[field_name].label = field_name.replace('_', ' ').title()

    def clean(self):
        cleaned_data = super().clean()
        # Only add our custom validation if there are no existing errors
        if not self.errors:
            # Check required fields in order
            for field in ['email', 'first_name', 'last_name', 'username', 'password1', 'password2']:
                if not cleaned_data.get(field):
                    self.add_error(field, f'This field is required.')
                    break  # Stop at the first empty field
        return cleaned_data

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style all fields with Bootstrap classes
        for field_name in ['username', 'password']:
            placeholder = {
                'password': 'Enter your password'
            }.get(field_name, f'Enter your {field_name}')
            
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control rabble-input',
                'placeholder': placeholder
            })
            # Remove the default label suffix
            self.fields[field_name].label_suffix = ''
            # Set the label class
            self.fields[field_name].label = field_name.replace('_', ' ').title()

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('Please enter your password')
        return password

class RabbleForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Members"
    )

    class Meta:
        model = Rabble
        fields = [
            'community_id',
            'description',
            'private',
            'members',
        ]
        widgets = {
            'community_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter community ID (no spaces allowed)…',
                'pattern': '[^\\s]*',
                'title': 'Community ID cannot contain spaces'
            }),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'What is this Rabble about?'}),
            'private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'community_id': 'Community ID',
            'description': 'Description',
            'private': 'Private Rabble?',
            'members': 'Members',
        }

    def clean_community_id(self):
        community_id = self.cleaned_data.get('community_id')
        if ' ' in community_id:
            raise forms.ValidationError("Community ID cannot contain spaces.")
        return community_id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['members'].queryset = User.objects.all()

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if username and email:
            try:
                user = User.objects.get(username=username, email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("No account found with this username and email combination.")
        
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

class ProfileEditForm(forms.ModelForm):
    current_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter current password to confirm changes'
        })
    )
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        current_password = cleaned_data.get('current_password')

        if new_password or confirm_password:
            if not current_password:
                raise forms.ValidationError("Please enter your current password to change your password.")
            if not self.instance.check_password(current_password):
                raise forms.ValidationError("Current password is incorrect.")
            if new_password != confirm_password:
                raise forms.ValidationError("New passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = supe9r().save(commit=False)
        if self.cleaned_data.get('new_password'):
            user.set_password(self.cleaned_data['new_password'])
        if commit:
            user.save()
        return user