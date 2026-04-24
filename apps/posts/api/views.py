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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
    
    @swagger_auto_schema(
        operation_summary="Список постов",
        operation_description="Получить список постов с фильтрацией и сортировкой",
        manual_parameters=[
            openapi.Parameter(
                'author',
                openapi.IN_QUERY,
                description="Фильтрация по ID автора",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'created_at',
                openapi.IN_QUERY,
                description="Фильтрация по дате создания",
                type=openapi.TYPE_STRING,
                format='date'
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Сортировка: created_at, likes_count, title. Используйте '-' для порядка",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Создание поста",
        operation_description="Создать новый пост",
        request_body=PostSerializer,
        responses={201: PostSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить пост по ID",
        operation_description="Получить один пост по его ID",
        responses={200: PostSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить пост",
        operation_description="Полное обновление существующего поста",
        request_body=PostSerializer,
        responses={200: PostSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление поста",
        operation_description="Частичное обновление существующего поста",
        request_body=PostSerializer,
        responses={200: PostSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить пост",
        operation_description="Удалить пост по его ID",
        responses={204: openapi.Response('Пост удалён')}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    @swagger_auto_schema(
        operation_summary="Список лайков",
        operation_description="Получить список лайков"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать лайк",
        operation_description="Создать новый лайк",
        request_body=LikeSerializer,
        responses={201: LikeSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить лайк по ID",
        operation_description="Получить один лайк по его ID",
        responses={200: LikeSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить лайк",
        operation_description="Полное обновление существующего лайка",
        request_body=LikeSerializer,
        responses={200: LikeSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление лайка",
        operation_description="Частичное обновление существующего лайка",
        request_body=LikeSerializer,
        responses={200: LikeSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить лайк",
        operation_description="Удалить лайк по его ID",
        responses={204: openapi.Response('Лайк удалён')}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
