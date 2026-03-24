from django.db import models


class Mood(models.TextChoices):
    HAPPY = 'HAPPY', 'Happy'
    SAD = 'SAD', 'Sad'
    CALM = 'CALM', 'Calm'
    ENERGETIC = 'ENERGETIC', 'Energetic'


class Genre(models.TextChoices):
    ROCK = 'ROCK', 'Rock'
    POP = 'POP', 'Pop'
    HIPHOP = 'HIPHOP', 'Hip-Hop'
    JAZZ = 'JAZZ', 'Jazz'
    COUNTRY = 'COUNTRY', 'Country'


class VoiceType(models.TextChoices):
    MALE = 'MALE', 'Male'
    FEMALE = 'FEMALE', 'Female'


class Occasion(models.TextChoices):
    BIRTHDAY = 'BIRTHDAY', 'Birthday'
    WEDDING = 'WEDDING', 'Wedding'
    PARTY = 'PARTY', 'Party'
    STUDYING = 'STUDYING', 'Studying'
