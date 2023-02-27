from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
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


# class ArticleDetailView(DetailView):
#     template_name = 'sports_news/article.html'
#     model         = Article

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(object_list=object_list, **kwargs)
#         context['category_list'] = Category.objects.all()
#         return context


def article_view(request, slug):
    article = get_object_or_404(Article, slug=slug)

    comments = article.comments.get_queryset()

    context = {'article': article,
               'category_list': Category.objects.all(),
               'selected_category': article.category,
               'comments': comments}

    return render(request, 'sports_news/article.html', context)


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'content', 'tags', 'category']

    def has_permission(self):
        # TODO use groups and permissions instead of a db table
        return hasattr(self.request.user, 'author')

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been created successfully.')
        return reverse_lazy('sports_news_app:index')

    def form_valid(self, form):
        obj = form.save(commit=False)
        print(self.request.user.author)
        obj.author = self.request.user.author
        obj.slug = slugify(form.cleaned_data['title'])
        obj.save()
        return super().form_valid(form)


class TagDetailView(DetailView):
    template_name = 'sports_news/articles_by_tag.html'
    model         = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_list'] = self.get_object().articles.all()
        context['category_list'] = Category.objects.all()
        context['selected_category'] = None
        return context


class CategoryDetailView(DetailView):
    template_name = 'sports_news/articles_by_category.html'
    model         = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_list'] = self.get_object().articles.all()
        context['category_list'] = Category.objects.all()
        context['selected_category'] = self.get_object()
        return context
