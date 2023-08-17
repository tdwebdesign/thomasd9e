from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    ReplyCreateView,
)

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("create/", PostCreateView.as_view(), name="post-create"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
    path("<slug:slug>/edit/", PostUpdateView.as_view(), name="post-edit"),
    path("<slug:slug>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("<slug:slug>/comment/", CommentCreateView.as_view(), name="comment-create"),
    path(
        "<slug:slug>/comment/<int:comment_id>/reply/",
        ReplyCreateView.as_view(),
        name="comment-reply",
    ),
]
