from django.db import models
from django.contrib.auth.models import User
import simple_history as sh

sh.register(User)

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # NOTE: история изменений объекта
    history = sh.models.HistoricalRecords()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name        = 'Автор'
        verbose_name_plural = 'Авторы'
        # TODO use this permission somehow
        permissions = (
            ('moderate_articles', 'Право модерировать статьи'),
        )


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    history = sh.models.HistoricalRecords()
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


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    history = sh.models.HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    DRAFT = 0
    PUBLISHED = 1
    STATUS_CHOICES = (
        (0, "Черновик"),     # The default status
        (1, "Опубликовано")
    )

    title      = models.CharField(max_length=200, unique=True, null=True)
    slug       = models.SlugField(max_length=200, unique=True, null=True)
    author     = models.ForeignKey(Author, null=True, blank=True, on_delete=models.SET_NULL, related_name='articles')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    content    = models.TextField(null=True)
    status     = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    tags       = models.ManyToManyField(Tag, blank=True, related_name='articles')
    category   = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='articles')
    history    = sh.models.HistoricalRecords()

    def __str__(self):
        return self.title

    class Meta:
        ordering            = ['-created_on']
        verbose_name        = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    article    = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author     = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='comments')
    created_on = models.DateTimeField(auto_now_add=True)
    body       = models.TextField()
    active     = models.BooleanField(default=True)
    history    = sh.models.HistoricalRecords()

    def __str__(self):
        if not self.body:
            return ''
        if len(self.body) < 50:
            return self.body
        return self.body[:47] + '...'

    class Meta:
        ordering = ['created_on']
        verbose_name        = 'Комментарий'
        verbose_name_plural = 'Комментарии'

# TODO News, Regular user
