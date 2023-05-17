from .models import Post, Comment
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"      # [ "writer", "content" ] 로 일부 지정 가능

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [ "writer", "content" ]