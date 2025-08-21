from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    password_expiration_date = forms.DateField(label="Дата истечения пароля:", widget=forms.DateInput(attrs={'type': 'date'}))
    comment = forms.CharField(label="Комментарий:", widget=forms.Textarea(attrs={'rows':12, 'cols':80}), required=False)
    plain_password = forms.CharField(label="Пароль (открытый текст)", required=False)
    email = forms.EmailField(label="Электронная почта", required=False)
    phone = forms.CharField(label="Телефон (формат: (000)111-22-22)", required=False)

    MESSENGER_CHOICES = [
        ('', '—'),
        ('Telegram', 'Telegram'),
        ('WhatsApp', 'WhatsApp'),
        ('Viber', 'Viber'),
        ('Signal', 'Signal'),
        ('VK', 'VK'),
        ('Другое', 'Другое'),
    ]
    preferred_messenger = forms.ChoiceField(label="Предпочитаемый мессенджер", choices=MESSENGER_CHOICES, required=False)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'plain_password', 'password1', 'password2', 'password_expiration_date', 'comment', 'preferred_messenger']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class CustomUserChangeForm(forms.ModelForm):
    MESSENGER_CHOICES = [
        ('', '—'),
        ('Telegram', 'Telegram'),
        ('WhatsApp', 'WhatsApp'),
        ('Viber', 'Viber'),
        ('Signal', 'Signal'),
        ('VK', 'VK'),
        ('Другое', 'Другое'),
    ]
    preferred_messenger = forms.ChoiceField(label="Предпочитаемый мессенджер", choices=MESSENGER_CHOICES, required=False)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'plain_password', 'password', 'comment', 'password_expiration_date', 'file', 'preferred_messenger']