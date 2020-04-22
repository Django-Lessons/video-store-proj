import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    paid_until = models.DateField(
        null=True,
        blank=True
    )

    def has_paid(
        self,
        current_date=datetime.date.today()
    ):
        if self.paid_until is None:
            return False

        return current_date < self.paid_until


class Video(models.Model):

    title = models.CharField(max_length=30)
    thumbnail = models.FileField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1
    )

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def __str__(self):
        return f"{self.title}"
