from rest_framework import serializers
from apps.posts.models.post import Post
from apps.posts.models.like import Like

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'