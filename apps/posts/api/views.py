from rest_framework.viewsets import ModelViewSet
from apps.posts.models.post import Post
from apps.posts.models.like import Like
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, LikeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PostFilter
from django.db.models import Count
from rest_framework.filters import OrderingFilter

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PostFilter

    ordering_fields = ['created_at', 'likes_count', 'title']
    ordering = ['-created_at']  # сортировка по умолчанию

    def get_queryset(self):
        return Post.objects.annotate(
            likes_count=Count('likes')
        )

class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer