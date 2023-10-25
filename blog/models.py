from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from taggit.models import Tag


class Post(models.Model):
    title = models.CharField(max_length=512)
    body = models.TextField(max_length=20000)
    date_publish = models.DateTimeField(auto_now_add=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='posts', null=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=2048)

    def __str__(self):
        return f'{self.user} comment: {self.post}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    is_liked = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user} like: {self.post}'


class Subscription(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    subscribe = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} follower: {self.author}'
