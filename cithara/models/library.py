from django.db import models
from .song_creator import SongCreator


class Library(models.Model):
    owner = models.OneToOneField(SongCreator, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.name}'s Library"
