from rest_framework.viewsets import ModelViewSet
from apps.posts.models.post import Post
from apps.posts.models.like import Like
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, LikeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PostFilter

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer