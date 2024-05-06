from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class ApplicationUser(AbstractUser):
    user_description = models.TextField(null=False, blank=True)
    quote = models.CharField(max_length=255, null=False, blank=True)
