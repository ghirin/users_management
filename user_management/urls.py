from users import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', views.home, name='home'), 
    path('password_change/', 
         auth_views.PasswordChangeView.as_view(success_url='/users/password_change/done/'), 
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/profile/', views.my_profile, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),  # Подключаем стандартные маршруты аутентификации
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
