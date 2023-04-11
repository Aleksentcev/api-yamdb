from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = [
    ('usr', 'user'),
    ('mdr', 'moderator'),
    ('adm', 'admin')
]


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=3,
        choices=ROLE_CHOICES,
        default='user'
    )
