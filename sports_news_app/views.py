from django.views.generic.list import ListView
from django.views.generic import DetailView
from .models import Article, Tag


class IndexListView(ListView):
    template_name = 'sports_news/index.html'
    model         = Article
    paginate_by   = 10

    return render(request, 'sports_news/index.html', context)


class TagDetailView(DetailView):
    template_name = 'sports_news/articles_by_tag.html'
    model         = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_list'] = self.get_object().articles.all()
        return context
