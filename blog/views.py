from django.db.models import F, Count
from django.db.models.functions import Substr
from rest_framework.response import Response

from .serializers import PostSerializer, CommentSerializer, SubscriptionSerializer, LikeSerializer, PostCreateSerializer
from .models import Post, Comment, Subscription, Like
from rest_framework import viewsets, generics, status, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['tags__name']
    ordering_fields = ['rating']
    search_fields = ['title', 'body']

    def get_queryset(self):
        queryset = self.queryset.annotate(
            rating=Count(F('ratings'))
        ).annotate(
            summary=Substr('body', 1, 100)
        )
        return queryset


class CreatePostAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.id == int(request.data.get('author')):
            return super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.id == int(request.data.get('user')):
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        user = request.user
        if int(request.data.get('user')) == user:
            return super().update(request, *args, **kwargs)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if instance.user == user:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateSubApiView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.id == int(request.data.get('user')):
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateLikeApiView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
