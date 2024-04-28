from django.db import models
from users.models import ApplicationUser


# Create your models here.

class Link(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    button_text = models.CharField(max_length=100, null=False, blank=False, default="Click here")
    destination = models.URLField(unique=True, null=False, blank=False)

    user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}: {self.name}"
