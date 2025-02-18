from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    password_expiration_date = forms.DateField(label="Дата истечения пароля:", widget=forms.DateInput(attrs={'type': 'date'}))
    comment = forms.CharField(label="Пароль или коммментарий:", widget=forms.Textarea(attrs={'rows':12, 'cols':80}), required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'password_expiration_date', 'comment']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'comment', 'password_expiration_date', 'file']