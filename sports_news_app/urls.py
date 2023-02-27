from django.urls import path

from . import views

app_name = 'sports_news_app'
urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('tags/<slug:slug>', views.TagDetailView.as_view(), name='articles-by-tag'),
    path('category/<slug:slug>', views.CategoryDetailView.as_view(), name='articles-by-category'),
    # path('articles/<slug:slug>', views.ArticleDetailView.as_view(), name='article'),
    path('articles/<slug:slug>', views.article_view, name='article'),
    path('create-article/', views.ArticleCreateView.as_view(), name='create-article'),
    path('articles/<slug:slug>/update', views.ArticleUpdateView.as_view(), name='update-article'),
]
