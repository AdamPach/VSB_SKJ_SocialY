from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class ApplicationUser(AbstractUser):
    user_description = models.TextField(null=False, blank=True)
    quote = models.CharField(max_length=255, null=False, blank=True)


class Follow(models.Model):
    source = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE, related_name="follow_source")

    destination = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE, related_name="follow_destination")

    class Meta:
        unique_together = ["source", "destination"]
        indexes = [
            models.Index(fields=["source", "source"], name="idx_unique_follow")
        ]
