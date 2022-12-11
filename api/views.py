from django.contrib.admin import action
from rest_framework.response import Response
from rest_framework.decorators import api_view

from sports_news_app.models import Article
from .serializers import ArticleSerializer

# TODO seems like I have to use `action` decorator instead
@api_view(['GET'])
def getData(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addArticle(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    # TODO else, response with error

    return Response(serializer.data)
