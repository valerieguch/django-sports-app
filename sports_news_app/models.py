from django.db import models
from django.utils import timezone

class Article(models.Model):
    title   = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    # TODO if I need to edit `created`, use this:
    # created = models.DateTimeField(default=timezone.now),

    def __str__(self):
        return self.title

    class Meta:
        verbose_name        = 'Статья'
        verbose_name_plural = 'Статьи'
