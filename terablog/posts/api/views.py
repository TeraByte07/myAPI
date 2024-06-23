from rest_framework import generics
from posts.api.serializers import PostSerializer, AuthorSerializer, CommentSerializer
from posts.models import Post, Comment, Author
from rest_framework.exceptions import ValidationError
from posts.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly

class PostCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        try:
            author = Author.objects.get(user=user)
        except Author.DoesNotExist:
            raise ValidationError("Only authors can create posts.")
        serializer.save(author=author)

class PostListView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'

# class AuthorListView(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = AuthorSerializer
#     queryset = Author.objects.all()

# class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = AuthorSerializer
#     queryset = Author.objects.all()

class CommentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('slug')

        # Debug information to ensure the correct post_id is retrieved
        print(f"Creating comment for post with ID: {post_id}")

        try:
            post = Post.objects.get(slug=post_id)
        except Post.DoesNotExist:
            raise ValidationError("Post matching query does not exist")

        comment_user = self.request.user
        comment_queryset = Comment.objects.filter(post=post, comment_user=comment_user)

        if comment_queryset.exists():
            raise ValidationError("You have already dropped a review for this post!!!")
        
        if post.number_rating == 0:
            post.avg_rating = serializer.validated_data["rating"]
            
        else:
            post.avg_rating = (post.avg_rating + serializer.validated_data['rating']) / 2

        post.number_rating = post.number_rating + 1
        post.save()

        serializer.save(post=post, comment_user=comment_user)

class CommentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Comment.objects.filter(post__slug=slug)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsReviewUserOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
