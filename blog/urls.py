from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, CommentViewSet, CreateSubApiView, CreateLikeApiView, CreatePostAPIView

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('subscribe/', CreateSubApiView.as_view()),
    path('liking/', CreateLikeApiView.as_view()),
    path('create-post/', CreatePostAPIView.as_view()),
    path('auth/', include('rest_framework.urls'))
]



