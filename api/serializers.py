from rest_framework import serializers
from sports_news_app.models import Article
from django.contrib.auth.models import User, Group

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # fields = '__all__'
        # fields = ["title", "slug", "author", "created_on", "updated_on", "content", "status", "tags",]
        fields = ["title", "slug", "author", "created_on", "updated_on", "status", "tags"]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
