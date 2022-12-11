from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),  # TODO read about path()
    path('add/', views.addArticle)
]
