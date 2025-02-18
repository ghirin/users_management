from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    password_expiration_date = models.DateField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='user_files/', null=True, blank=True)  # Add this line

    def __str__(self):
        return self.username
    
class UserFile(models.Model):
    user = models.ForeignKey(CustomUser, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='user_files/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    pass

User = get_user_model()