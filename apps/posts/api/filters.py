import django_filters
from apps.posts.models import Post


class PostFilter(django_filters.FilterSet):
    # фильтр по автору (по id)
    author = django_filters.NumberFilter(field_name='author__id')

    # фильтр по дате (диапазон)
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['author']