from django.shortcuts import render
from .models import Article


def index(request):
    # TODO pagination?
    articles = Article.objects.all().order_by('-created_on')[:20]
    context = {'articles': articles}

    return render(request, 'sports_news/index.html', context)
