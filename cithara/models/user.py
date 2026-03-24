from django.db import models
from .google_account import GoogleAccount


class User(models.Model):
    google_account = models.OneToOneField(GoogleAccount, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
