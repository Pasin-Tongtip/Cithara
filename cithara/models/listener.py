from django.db import models
from .user import User


class Listener(User):
    def __str__(self):
        return f"Listener: {self.name}"
