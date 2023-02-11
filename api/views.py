# from django.contrib.admin import action
from django.contrib.auth.models import User, Group

from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action

from sports_news_app.models import Author, Tag, Article, Comment
from .serializers import  UserSerializer, GroupSerializer, AuthorSerializer, TagSerializer, ArticleSerializer, CommentSerializer

import json

# TODO seems like I have to use `action` decorator instead
# @api_view(['GET'])
# def getArticles(request):
#     articles = Article.objects.all()
#     serializer = ArticleSerializer(articles, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# def addArticle(request):
#     serializer = ArticleSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     # TODO else, response with error

#     return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # TODO allow only article moderators
    permission_classes = [permissions.IsAuthenticated]

    # NOTE: метод для списка
    @action(methods=['GET'], detail=False)
    def stats(self, request):
        data = dict()
        data['total_count'] = self.queryset.count()
        data['published_count'] = self.queryset.filter(status=Article.PUBLISHED).count()
        return Response(data)

    # NOTE: метод для одного объекта
    @action(methods=['POST'], detail=True)
    def set_status(self, request, pk=None):
        if "status" not in request.data:
            return Response({"detail": "Ключ \"status\" не найден"},
                            status=status.HTTP_400_BAD_REQUEST)

        article_status = request.data["status"]
        if article_status == "draft" and article_status == "published":
            return Response({"detail": "Неизвестный \"status\""},
                            status=status.HTTP_400_BAD_REQUEST)

        article = self.get_object()
        article.status = Article.DRAFT if article_status == "draft" else Article.PUBLISHED
        article.save()

        return Response({"detail": "Статус успешно установлен"})


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
