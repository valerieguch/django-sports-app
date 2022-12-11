from django.contrib import admin
from .models import Author, Tag, Article

# admin.site.register(Article)

@admin.register(Author)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['user__icontains',]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ('status',)
    search_fields = ['title__icontains', 'content__icontains']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name__icontains',]
    prepopulated_fields = {'slug': ('name',)}
