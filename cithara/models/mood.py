from django.db import models


class Mood(models.TextChoices):
    HAPPY = 'HAPPY', 'Happy'
    SAD = 'SAD', 'Sad'
    CALM = 'CALM', 'Calm'
    ENERGETIC = 'ENERGETIC', 'Energetic'
