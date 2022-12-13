from rest_framework import serializers
from sports_news_app.models import Author, Tag, Article, Comment
from django.contrib.auth.models import User, Group


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        # fields = '__all__'
        fields = ['user']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        # fields = '__all__'
        fields = ['name', 'slug']

    # TODO maybe this should be active only with POST or UPDATE requests?
    def validate_name(self, name):
        if len(name) < 3:
            raise serializers.ValidationError("Имя тега короче 3 знаков.")
        return True


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        # fields = '__all__'
        fields = ["title", "slug", "author", "created_on", "updated_on", "content", "status", "tags"]


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        # fields = '__all__'
        fields = ["article", "author", "created_on", "body", "active"]
