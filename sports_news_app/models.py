from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name        = 'Автор'
        verbose_name_plural = 'Авторы'


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    # article = models.ForeignKey(
    #     Article,
    #     null=True,
    #     on_delete=models.CASCADE,
    #     related_name='tags',
    #     related_query_name='tag',
    # )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = 'Тег'
        verbose_name_plural = 'Теги'


STATUS = (
    (0, "Черновик"),
    (1, "Опубликовано")
)

class Article(models.Model):
    title      = models.CharField(max_length=200, unique=True, null=True)
    slug       = models.SlugField(max_length=200, unique=True, null=True)
    author     = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name='articles')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    content    = models.TextField(null=True)
    status     = models.IntegerField(choices=STATUS, default=0)
    tags       = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name        = 'Статья'
        verbose_name_plural = 'Статьи'

# TODO News, User, Comment
