# from django.contrib.admin import action
from django.contrib.auth.models import User, Group

from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action

from sports_news_app.models import Author, Tag, Category, Article, Comment
from .serializers import UserSerializer, GroupSerializer, AuthorSerializer, TagSerializer, CategorySerializer, ArticleSerializer, CommentSerializer

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
    # NOTE: фильтрация - SearchFilter
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']


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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # TODO allow only article moderators
    permission_classes = [permissions.IsAuthenticated]

    # NOTE: фильтрация по GET параметрам в URL
    # Пример: api/articles/?author=vasily
    def get_queryset(self):
        queryset = self.queryset
        author = self.request.query_params.get('author')
        if author is not None:
            queryset = queryset.filter(author__user__username=author)
        return queryset

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
        # TODO this should be done with a custom serializer
        if "status" not in request.data:
            return Response({"detail": "Ключ \"status\" не найден"},
                            status=status.HTTP_400_BAD_REQUEST)

        article_status = request.data["status"]
        if article_status != "draft" and article_status != "published":
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

    # NOTE: фильтрация - результаты, относящиеся к текущему пользователю
    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(author=user)
