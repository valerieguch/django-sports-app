from django.views.generic.list import ListView
from .models import Article


class IndexListView(ListView):
    template_name = 'sports_news/index.html'
    model         = Article
    paginate_by   = 10

    return render(request, 'sports_news/index.html', context)
