from django.contrib import admin
from .models import GoogleAccount, SongCreator, Listener, Library, Song

admin.site.register(GoogleAccount)
admin.site.register(SongCreator)
admin.site.register(Listener)
admin.site.register(Library)
admin.site.register(Song)
