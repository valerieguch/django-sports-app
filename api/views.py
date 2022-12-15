# from django.contrib.admin import action
from django.contrib.auth.models import User, Group

from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action

from sports_news_app.models import Author, Tag, Article, Comment
from .serializers import  UserSerializer, GroupSerializer, AuthorSerializer, TagSerializer, ArticleSerializer, CommentSerializer


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
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['GET'], detail=False)
    def get_data(self, request, **kwargs):
        data = dict()
        data['info'] = 'тут можем вернуть какие-то данные'
        return Response(data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
