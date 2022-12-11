from django.contrib import admin
from .models import Author, Tag, Article, Comment


@admin.register(Author)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['user__icontains',]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'tags_list', 'status','created_on')
    list_filter = ('status',)
    search_fields = ['title__icontains', 'content__icontains']
    prepopulated_fields = {'slug': ('title',)}

    def tags_list(self, obj):
        return ", ".join([t.name for t in obj.tags.all()])


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name__icontains',]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'article')
    search_fields = ['body__icontains',]
