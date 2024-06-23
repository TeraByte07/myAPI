from django.urls import path
from posts.api.views import PostListView, PostDetailView, PostCreateView,CommentListView, CommentDetailView, CommentCreateView#,  AuthorListView, AuthorDetailView

urlpatterns = [
    path("post-create/", PostCreateView.as_view(), name="post-create"),
    path("lists/", PostListView.as_view(), name="post-lists"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post-details"),
    # path("author/lists/", AuthorListView.as_view(), name="author-lists"),
    # path("author/<int:pk>/", AuthorDetailView.as_view(), name="author-details"),
    path("<slug:slug>/comment-create/", CommentCreateView.as_view(), name="comment-create"),
    path("<slug:slug>/comments/", CommentListView.as_view(), name="comment-lists"),
    path("<slug:slug>/comment/<int:pk>/", CommentDetailView.as_view(), name="comment-details"),
]
