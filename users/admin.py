from django.contrib import admin
from .models import CustomUser, UserFile
from django import forms

class UserFileInline(admin.TabularInline):
    model = UserFile
    extra = 1

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'comment', 'password_expiration_date']

class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserForm
    list_display = ('username', 'email', 'password', 'password_expiration_date', 'comment', 'is_active')
    search_fields = ['username', 'email']
    list_filter = ['is_active']
    inlines = [UserFileInline]
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Profile', {'fields': ('comment', 'password_expiration_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserFile)
