from rest_framework.viewsets import ModelViewSet
from apps.posts.models.post import Post
from apps.posts.models.like import Like
from .serializers import PostSerializer, LikeSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer