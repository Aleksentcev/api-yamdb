from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

USER = ('user', 'Пользователь')
MODERATOR = ('moderator', 'Модератор')
ADMIN = ('admin', 'Администратор')

ROLE_CHOICES = [
    USER,
    MODERATOR,
    ADMIN
]


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')]
    )
    email = models.EmailField(
        'Адрес эл.почты',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField('О себе', blank=True)
    role = models.CharField(
        'Права пользователя',
        choices=ROLE_CHOICES,
        default=USER[0],
        max_length=10
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == MODERATOR[0]

    @property
    def is_admin(self):
        return self.role == ADMIN[0]
