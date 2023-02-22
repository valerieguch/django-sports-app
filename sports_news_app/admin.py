from django.contrib import admin
from .models import Author, Tag, Article, Comment
from import_export.admin import ImportMixin, ExportActionMixin
from simple_history.admin import SimpleHistoryAdmin


# NOTE: импорт и экспорт данных из админки
# NOTE: история изменений объекта (админка)
@admin.register(Author)
class AuthorAdmin(ImportMixin, ExportActionMixin, SimpleHistoryAdmin):
    search_fields = ['user__username__icontains',
                     'user__first_name__icontains',
                     'user__last_name__icontains']


@admin.register(Article)
class ArticleAdmin(ImportMixin, ExportActionMixin, SimpleHistoryAdmin):
    list_display = ('title', 'tags_list', 'status','created_on')
    list_filter = ('status',)
    search_fields = ['title__icontains', 'content__icontains']
    prepopulated_fields = {'slug': ('title',)}

    def tags_list(self, obj):
        return ", ".join([t.name for t in obj.tags.all()])


@admin.register(Tag)
class TagAdmin(ImportMixin, ExportActionMixin, SimpleHistoryAdmin):
    search_fields = ['name__icontains',]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(ImportMixin, ExportActionMixin, SimpleHistoryAdmin):
    list_display = ('author', 'body', 'article')
    search_fields = ['body__icontains',]
