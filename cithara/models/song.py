from django.db import models
from .genre import Genre
from .library import Library
from .mood import Mood
from .occasion import Occasion
from .voice_type import VoiceType


class Song(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='songs')
    title = models.CharField(max_length=200)
    mood = models.CharField(max_length=20, choices=Mood.choices)
    genre = models.CharField(max_length=20, choices=Genre.choices)
    story = models.TextField()
    voice_type = models.CharField(max_length=20, choices=VoiceType.choices)
    occasion = models.CharField(max_length=20, choices=Occasion.choices)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.library.owner.name}"
