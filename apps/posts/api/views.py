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
    
    # Документация
    # GET
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
        ],
        responses={
            200: openapi.Response(
                description="Список постов",
                schema=PostSerializer(many=True),
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "author": 1,
                            "title": "Пример заголовка поста",
                            "body": "Это пример текста поста. Здесь может быть любое содержание.",
                            "created_at": "2024-01-15T10:30:00Z",
                            "updated_at": "2024-01-15T10:30:00Z"
                        },
                        {
                            "id": 2,
                            "author": 2,
                            "title": "Второй пост",
                            "body": "Текст второго поста с другим содержанием.",
                            "created_at": "2024-01-14T08:15:00Z",
                            "updated_at": "2024-01-14T08:15:00Z"
                        }
                    ]
                }
            )
        }
    
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    # POST
    @swagger_auto_schema(
        operation_summary="Создание поста",
        operation_description="Создать новый пост",
        request_body=PostSerializer,
        responses={
            201: openapi.Response(
                description="Пост создан",
                schema=PostSerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "author": 1,
                        "title": "Пример заголовка поста",
                        "body": "Это пример текста поста. Здесь может быть любое содержание.",
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T10:30:00Z"
                    }
                }
            )
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    # GET id
    @swagger_auto_schema(
        operation_summary="Получить пост по ID",
        operation_description="Получить один пост по его ID",
        responses={
            200: openapi.Response(
                description="Пост найден",
                schema=PostSerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "author": 1,
                        "title": "Пример заголовка поста",
                        "body": "Это пример текста поста. Здесь может быть любое содержание.",
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T10:30:00Z"
                    }
                }
            )
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # PUT
    @swagger_auto_schema(
        operation_summary="Обновить пост",
        operation_description="Полное обновление существующего поста",
        request_body=PostSerializer,
        responses={
            200: openapi.Response(
                description="Пост обновлён",
                schema=PostSerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "author": 1,
                        "title": "Обновлённый заголовок поста",
                        "body": "Обновлённый текст поста с новым содержанием.",
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-16T14:20:00Z"
                    }
                }
            )
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    # PATCH
    @swagger_auto_schema(
        operation_summary="Частичное обновление поста",
        operation_description="Частичное обновление существующего поста",
        request_body=PostSerializer,
        responses={
            200: openapi.Response(
                description="Пост обновлён",
                schema=PostSerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "author": 1,
                        "title": "Обновлённый заголовок",
                        "body": "Это пример текста поста. Здесь может быть любое содержание.",
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-16T14:20:00Z"
                    }
                }
            )
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # DELETE
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

    # Документация
    # GET
    @swagger_auto_schema(
        operation_summary="Список лайков",
        operation_description="Получить список лайков",
        responses={
            200: openapi.Response(
                description="Список лайков",
                schema=LikeSerializer(many=True),
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "post": 1,
                            "user": 1
                        },
                        {
                            "id": 2,
                            "post": 1,
                            "user": 2
                        }
                    ]
                }
            )
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # POST
    @swagger_auto_schema(
        operation_summary="Создать лайк",
        operation_description="Создать новый лайк",
        request_body=LikeSerializer,
        responses={
            201: openapi.Response(
                description="Лайк создан",
                schema=LikeSerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "post": 1,
                        "user": 1
                    }
                }
            )
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # GET id
    @swagger_auto_schema(
        operation_summary="Получить лайк по ID",
        operation_description="Получить один лайк по его ID",
        responses={
            200: openapi.Response(
                description="Лайк найден",
                schema=LikeSerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "post": 1,
                        "user": 1
                    }
                }
            )
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # PUT
    @swagger_auto_schema(
        operation_summary="Обновить лайк",
        operation_description="Полное обновление существующего лайка",
        request_body=LikeSerializer,
        responses={
            200: openapi.Response(
                description="Лайк обновлён",
                schema=LikeSerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "post": 2,
                        "user": 1
                    }
                }
            )
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # PATCH
    @swagger_auto_schema(
        operation_summary="Частичное обновление лайка",
        operation_description="Частичное обновление существующего лайка",
        request_body=LikeSerializer,
        responses={
            200: openapi.Response(
                description="Лайк обновлён",
                schema=LikeSerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "post": 2,
                        "user": 1
                    }
                }
            )
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # DELETE
    @swagger_auto_schema(
        operation_summary="Удалить лайк",
        operation_description="Удалить лайк по его ID",
        responses={204: openapi.Response('Лайк удалён')}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
