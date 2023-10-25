from rest_framework import serializers

from blog.models import Post, Comment, Subscription, Like
from taggit.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    tags = TagSerializer(read_only=True, many=True)
    comments = CommentSerializer(many=True, read_only=True)
    rating = serializers.IntegerField()
    summary = serializers.CharField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'date_publish', 'author', 'tags', 'comments', 'rating', 'summary']


class PostCreateSerializer(serializers.ModelSerializer):
    tags = TagSerializer()

    class Meta:
        model = Post
        fields = ['author', 'title', 'body', 'tags']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        like, _ = Like.objects.update_or_create(
            post=validated_data.get('post', None),
            user=validated_data.get('user', None),
            defaults={'is_liked': validated_data.get('is_liked')}
        )

        return like
