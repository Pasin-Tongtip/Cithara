from django.db import models


# Enumerations
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


# Models
class GoogleAccount(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class User(models.Model):
    google_account = models.OneToOneField(GoogleAccount, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# User roles
class SongCreator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"Song creator: {self.name}"


class Listener(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"Listener: {self.name}"


class Library(models.Model):
    owner = models.OneToOneField(SongCreator, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.name}'s Library"


class Song(models.Model):
    # creator = models.ForeignKey(SongCreator, on_delete=models.CASCADE, related_name='songs')
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
