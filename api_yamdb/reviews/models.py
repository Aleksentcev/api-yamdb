from django.db import models
from users.models import User

SCORE_CHOICES = [
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
    ('6', 6),
    ('7', 7),
    ('8', 8),
    ('9', 9),
    ('10', 10),
]


class Category(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
    )
    slug = models.SlugField(
        'Адрес',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        default_related_name = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
    )
    slug = models.SlugField(
        'Адрес',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        default_related_name = 'genres'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=256,
    )
    year = models.IntegerField('Год создания произведения')
    description = models.TextField('Описание произведения', blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        default=1,
        verbose_name='Категория',
        help_text='Категория произведения',
    )

    class Meta:
        ordering = ('name',)
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_DEFAULT,
        default=1,
        verbose_name='Жанр',
        help_text='Жанр произведения',
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    text = models.TextField('Текст отзыва')
    score = models.CharField(
        'Оценка',
        max_length=5,
        choices=SCORE_CHOICES,
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        default_related_name = 'reviews'
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Обзор'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
