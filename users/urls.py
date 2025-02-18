from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .views import user_list

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),  # Подключаем стандартные маршруты аутентификации
    path('login/', views.user_login, name='login'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
#    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),  # Add this line
    path('logout/', views.logout_view, name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('create_user/', views.create_user, name='create_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/', user_list, name='user_list'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),

]