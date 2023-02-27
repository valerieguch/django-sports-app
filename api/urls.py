from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'articles', views.ArticleViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('articles/', views.getArticles),
    # path('add/', views.addArticle)
]
