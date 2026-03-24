from django.db import models


class Genre(models.TextChoices):
    ROCK = 'ROCK', 'Rock'
    POP = 'POP', 'Pop'
    HIPHOP = 'HIPHOP', 'Hip-Hop'
    JAZZ = 'JAZZ', 'Jazz'
    COUNTRY = 'COUNTRY', 'Country'
