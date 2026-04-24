from rest_framework import serializers
from apps.posts.models.post import Post
from apps.posts.models.like import Like
from apps.posts.models.comment import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'body', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'body', 'created_at', 'updated_at', 'comments', 'like_count']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_like_count(self, obj):
        return obj.likes.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'