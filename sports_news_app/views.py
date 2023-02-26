from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, render
from .models import Article, Tag, Category


# TODO show only published articles
class IndexListView(ListView):
    template_name = 'sports_news/index.html'
    model         = Article
    paginate_by   = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['category_list'] = Category.objects.all()
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

    context = {'article': article,
               'category_list': Category.objects.all()}

    return render(request, 'sports_news/article.html', context)


class TagDetailView(DetailView):
    template_name = 'sports_news/articles_by_tag.html'
    model         = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_list'] = self.get_object().articles.all()
        context['category_list'] = Category.objects.all()
        return context


class CategoryDetailView(DetailView):
    template_name = 'sports_news/articles_by_category.html'
    model         = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_list'] = self.get_object().articles.all()
        context['category_list'] = Category.objects.all()
        return context
