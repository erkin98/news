from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, CommentDetailSerializer


class PostScopedCommentMixin:
    post_lookup_url_kwarg = "pk"

    def get_post_id(self):
        return self.kwargs[self.post_lookup_url_kwarg]

    def get_base_queryset(self):
        return Comment.objects.for_post(self.get_post_id())

    def get_queryset(self):
        return self.get_base_queryset().ordered()


class UpvoteView(APIView):
    def post(self, *args, **kwargs):
        post_id = kwargs["pk"]
        post = get_object_or_404(Post, pk=post_id)
        Post.objects.filter(pk=post_id).update(votes=F("votes") + 1)
        return JsonResponse({"Succesfully upvoted": f"Article: {post.title}"})


class ListCreatePostAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyPostAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class ListCreateCommentAPIView(PostScopedCommentMixin, ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        return self.get_base_queryset().roots().ordered()

    def perform_create(self, serializer):
        serializer.save(article_id=self.get_post_id())


class RetrieveUpdateDestroyCommentAPIView(
    PostScopedCommentMixin, RetrieveUpdateDestroyAPIView
):
    post_lookup_url_kwarg = "id"
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class RetrieveUpdateDestroyCommentReplyAPIView(
    PostScopedCommentMixin, RetrieveUpdateDestroyAPIView
):
    post_lookup_url_kwarg = "id"
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
