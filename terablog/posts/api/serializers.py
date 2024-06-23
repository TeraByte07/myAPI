from rest_framework import serializers
from posts.models import Post, Author, Comment

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Post
        fields = "__all__"
        
class AuthorSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = "__all__"
        
class CommentSerializer(serializers.ModelSerializer):
    comment_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        exclude = ("post",)