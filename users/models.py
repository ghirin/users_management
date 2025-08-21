
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth import get_user_model

# Модель населённого пункта
class Locality(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="Населённый пункт")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Населённый пункт"
        verbose_name_plural = "Населённые пункты"
from django.core.validators import RegexValidator

# Пользователь
class CustomUser(AbstractUser):
    preferred_messenger = models.CharField('Предпочитаемый мессенджер', max_length=64, blank=True, null=True)
    password_expiration_date = models.DateField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)
    plain_password = models.CharField('Пароль (открытый текст)', max_length=128, blank=True, null=True)
    file = models.FileField(upload_to='user_files/', null=True, blank=True)
    email = models.EmailField('Электронная почта', blank=True, null=True)
    phone = models.CharField(
        'Телефон',
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\(\d{3}\)\d{3}-\d{2}-\d{2}$',
            message='Формат телефона: (000)111-22-22',
        )]
    )
    locality = models.ForeignKey(Locality, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Населённый пункт", related_name="users")

    def __str__(self):
        return self.username

# Файлы пользователя
class UserFile(models.Model):
    user = models.ForeignKey(CustomUser, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='user_files/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

User = get_user_model()