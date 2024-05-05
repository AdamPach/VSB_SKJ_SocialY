from django.db import models
from users.models import ApplicationUser


# Create your models here.

class Post(models.Model):
    post_content = models.TextField(max_length=1000, blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author.username}: {self.created_on}"


class Comment(models.Model):
    comment_content = models.TextField(max_length=1000, blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author.username}: {self.created_on}"


class Like(models.Model):
    liked_on = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes: {self.post.id}"

    class Meta:
        unique_together = ["user", "post"]
        indexes = [
            models.Index(fields=["user", "post"], name="like_user_post_index")
        ]
