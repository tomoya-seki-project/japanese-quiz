from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from django import forms

from .models import User


class RegistForm(forms.ModelForm):
    password2 = forms.CharField(label='Password(confirm)', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password',]
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    field_order = [
        'username',
        'email',
        'password',
        'password2',
    ]
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                self.add_error('password2', 'Password and Password(confirm) have to be the same')
            else:
                user = User(username=username, email=email)
                try:
                    validate_password(password1, user)
                except ValidationError as e:
                    self.add_error('password', e)

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email : ')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    remember_me = forms.BooleanField(label='Remember Me', required=False)