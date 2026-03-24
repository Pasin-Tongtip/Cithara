from django.test import TestCase
from django.db import IntegrityError
from .models import GoogleAccount, User, SongCreator, Listener, Library, Song, Mood, Genre, VoiceType, Occasion


class DomainModelTest(TestCase):
    def setUp(self):
        self.google_account = GoogleAccount.objects.create(email="test@gmail.com")
        self.user = User.objects.create(google_account=self.google_account)
        self.creator = SongCreator.objects.create(user=self.user)
        self.library = Library.objects.create(owner=self.creator)

    def test_one_creator_has_one_library(self):
        self.assertEqual(self.library.owner, self.creator)

    def test_create_song_success(self):
        song = Song.objects.create(
            creator=self.creator,
            library=self.library,
            title="Test Song",
            mood=Mood.HAPPY,
            genre=Genre.POP,
            story="Test context",
            voice_type=VoiceType.MALE,
            occasion=Occasion.PARTY
        )

        self.assertEqual(song.creator, self.creator)
        self.assertEqual(song.library, self.library)

    def test_library_have_multiple_song(self):
        Song.objects.create(
            creator=self.creator,
            library=self.library,
            title="Song 1",
            mood=Mood.HAPPY,
            genre=Genre.POP,
            story="Context 1",
            voice_type=VoiceType.MALE,
            occasion=Occasion.PARTY
        )

        Song.objects.create(
            creator=self.creator,
            library=self.library,
            title="Song 2",
            mood=Mood.SAD,
            genre=Genre.ROCK,
            story="Context 2",
            voice_type=VoiceType.FEMALE,
            occasion=Occasion.WEDDING
        )

        self.assertEqual(self.library.songs.count(), 2)

    def test_song_must_have_creator(self):
        with self.assertRaises(IntegrityError):
            Song.objects.create(
                creator=None,
                library=self.library,
                title="Invalid Song",
                mood=Mood.HAPPY,
                genre=Genre.POP,
                story="Context",
                voice_type=VoiceType.MALE,
                occasion=Occasion.PARTY
            )

    def test_song_must_have_library(self):
        with self.assertRaises(IntegrityError):
            Song.objects.create(
                creator=self.creator,
                library=None,
                title="Invalid Song",
                mood=Mood.HAPPY,
                genre=Genre.POP,
                story="Context",
                voice_type=VoiceType.MALE,
                occasion=Occasion.PARTY
            )

    def test_enumeration(self):
        with self.assertRaises(IntegrityError):
            Song.objects.create(
                creator=self.creator,
                library=None,
                title="Invalid Song",
                mood="WRONGMOOD",
                genre=Genre.POP,
                story="Context",
                voice_type=VoiceType.MALE,
                occasion=Occasion.PARTY
            )
