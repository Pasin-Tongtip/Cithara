from django.contrib import admin
from .models import GoogleAccount, User, SongCreator, Listener, Library, Song, Mood, Genre, VoiceType, Occasion

admin.site.register(GoogleAccount)
admin.site.register(User)
admin.site.register(SongCreator)
admin.site.register(Listener)
admin.site.register(Library)
admin.site.register(Song)
