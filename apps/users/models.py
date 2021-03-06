from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="users/profile_images/default_avatar.jpg", upload_to="users/profile_images/"
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
