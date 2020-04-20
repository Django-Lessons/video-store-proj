from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def is_pro_user(self):
        return False


class Video(models.Model):

    title = models.CharField(max_length=30)
    thumbnail = models.FileField()

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def __str__(self):
        return f"{self.title}"
