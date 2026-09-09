from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError

from django import forms

User = get_user_model()

class RegistForm(forms.ModelForm):
    password2 = forms.CharField(label='パスワード（確認用）', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',]
        labels = {
            'username': 'ユーザー名',
            'email': 'メールアドレス',
            'password': 'パスワード',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }
        error_messages = {
            "email": {"unique": "このメールアドレスはすでに登録されています。"},
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
                self.add_error('password2', 'パスワードが一致しません。')
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
        user.is_active = False
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    remember_me = forms.BooleanField(label='ログイン状態を保持', required=False)
    error_messages = {
        "invalid_login": (
            "メールアドレスまたはパスワードが正しくありません。"
            "メール認証が完了しているかもご確認ください。"
        ),
        "inactive": (
            "このアカウントは現在利用できません。"
        ),
    }

class UserChangeAdminForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='Password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser')

    def clean_password(self):
        return self.instance.password

class UserCreationAdminForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                self.add_error("password2", "The passwords do not match.")
            else:
                user = User(username=username, email=email)
                try:
                    validate_password(password1, user)
                except ValidationError as e:
                    self.add_error("password1", e)
        else:
            self.add_error(None, "Please fill in both password fields.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class ResendActivationEmailForm(forms.Form):
    email = forms.EmailField(
        label="メールアドレス",
        max_length=254,
    )
