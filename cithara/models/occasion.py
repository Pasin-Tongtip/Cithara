from django.db import models


class Occasion(models.TextChoices):
    BIRTHDAY = 'BIRTHDAY', 'Birthday'
    WEDDING = 'WEDDING', 'Wedding'
    PARTY = 'PARTY', 'Party'
    STUDYING = 'STUDYING', 'Studying'
