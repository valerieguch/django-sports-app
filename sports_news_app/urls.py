from django.urls import path

from . import views

app_name = 'sports_news_app'
urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('tags/<str:slug>', views.TagDetailView.as_view(), name='articles-by-tag'),
]
