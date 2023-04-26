from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput, label='Ім\'я користувача', max_length=254)
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    error_messages = {
        'invalid_login': 'Введіть коректне ім\'я користувача і пароль',
        'inactive': 'Цей аккаунт неактивний.',
        'invalid_password': 'Невірно введений пароль'
    }


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=101, label='Ім\'я')
    last_name = forms.CharField(max_length=101, label='Прізвище')
    email = forms.EmailField(required=True, label='Електронна пошта')
    password1 = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Підтвердження паролю', strip=False, widget=forms.PasswordInput)
    error_messages = {
        'password_mismatch': 'Паролі не співпадають.'
    }

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password1']
        labels = {
            'username': 'Псевдонім',
            'first_name': 'Ім`я',
            'last_name': 'Прізвище',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Повторно пароль'
        }

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', "Електронна пошта занята.")
            raise forms.ValidationError("Електронна пошта занята.")

        return self.cleaned_data

    def clean_username(self):
        data = self.cleaned_data['username']
        user_model = get_user_model()
        if user_model.objects.filter(username=data).exists():
            raise ValidationError("Ім'я користувача заняте.")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data
