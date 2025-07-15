from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_organizer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=True)  # افتراضياً المستخدم عميل
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username
