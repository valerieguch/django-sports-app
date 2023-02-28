from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import Http404, get_object_or_404, render
from django.urls import reverse_lazy
from unidecode import unidecode
from django.utils.text import slugify
from .models import Article, Tag, Category
from django.contrib import messages

# TODO show only published articles
class IndexListView(ListView):
    template_name = 'sports_news/index.html'
    model         = Article
    paginate_by   = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['category_list'] = Category.objects.all()
        context['selected_category'] = None
        return context

    def get_queryset(self):
        return Article.objects.filter(status=Article.PUBLISHED)


# class ArticleDetailView(DetailView):
#     template_name = 'sports_news/article.html'
#     model         = Article

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(object_list=object_list, **kwargs)
#         context['category_list'] = Category.objects.all()
#         return context


def article_view(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if article.status != Article.PUBLISHED and (
        not hasattr(request.user, 'author') or request.user.author != article.author
    ):
        raise Http404('Atricle not found')

    comments = article.comments.get_queryset()
    context = {
        'article': article,
        'category_list': Category.objects.all(),
        'selected_category': article.category,
        'comments': comments,
        'is_not_published': article.status != Article.PUBLISHED
    }

    return render(request, 'sports_news/article.html', context)


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model  = Article
    fields = ['title', 'content', 'tags', 'category', 'status']

    def has_permission(self):
        # TODO use groups and permissions instead of a db table
        return hasattr(self.request.user, 'author')

    def get_success_url(self):
        messages.success(self.request, 'Статья успешно создана.')
        return reverse_lazy('sports_news_app:article', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user.author
        obj.slug = slugify(unidecode(form.cleaned_data['title']))
        obj.save()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model  = Article
    fields = ['title', 'content', 'tags', 'category', 'status']

    def has_permission(self):
        # TODO use groups and permissions instead of a db table
        if not hasattr(self.request.user, 'author'):
            return False
        return self.get_object().author == self.request.user.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True

        return context

    def get_success_url(self):
        messages.success(self.request, 'Статья обновлена.')
        return reverse_lazy('sports_news_app:article', kwargs={'slug': self.object.slug})


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article

    def has_permission(self):
        # TODO use groups and permissions instead of a db table
        if not hasattr(self.request.user, 'author'):
            return False
        return self.get_object().author == self.request.user.author

    def get_success_url(self):
        messages.success(self.request, 'Статья удалена.')
        return reverse_lazy('sports_news_app:index')


class TagDetailView(DetailView):
    template_name = 'sports_news/articles_by_tag.html'
    model         = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_list'] = self.get_object().articles.filter(status=Article.PUBLISHED)
        context['category_list'] = Category.objects.all()
        context['selected_category'] = None
        return context


class CategoryDetailView(DetailView):
    template_name = 'sports_news/articles_by_category.html'
    model         = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_list'] = self.get_object().articles.filter(status=Article.PUBLISHED)
        context['category_list'] = Category.objects.all()
        context['selected_category'] = self.get_object()
        return context
