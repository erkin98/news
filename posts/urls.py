from django.urls import path
from . import views


urlpatterns = [
    path("posts/", views.ListCreatePostAPIView.as_view(), name="get_posts"),
    path(
        "posts/<int:pk>/",
        views.RetrieveUpdateDestroyPostAPIView.as_view(),
        name="get_delete_update_post",
    ),
    path(
        "posts/<int:pk>/upvote",
        views.UpvoteView.as_view(),
        name="get_delete_update_post",
    ),
    path(
        "posts/<int:pk>/comments/",
        views.ListCreateCommentAPIView.as_view(),
        name="get_post_comment",
    ),
    path(
        "posts/<int:id>/comments/<int:pk>/",
        views.RetrieveUpdateDestroyCommentAPIView.as_view(),
        name="get_delete_update_post_comment",
    ),
    path(
        "posts/<int:id>/comments/<int:pk>/replies",
        views.RetrieveUpdateDestroyCommentReplyAPIView.as_view(),
        name="get_delete_update_post_comment",
    ),
]
