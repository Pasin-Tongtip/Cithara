from django.db import models
from .user import User


class SongCreator(User):
    def __str__(self):
        return f"Song creator: {self.name}"
