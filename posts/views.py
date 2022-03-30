from django.http import JsonResponse
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, CommentDetailSerializer


class UpvoteView(APIView):
    def post(self, *args, **kwargs):
        data = Post.objects.get(id=kwargs['pk'])
        data.votes += 1
        data.save()
        return JsonResponse({'Succesfully upvoted': f'Article: {data.title}'})


class ListCreatePostAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyPostAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class ListCreateCommentAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        post_pk = self.kwargs["pk"]
        return Comment.objects.filter(article_id=post_pk, parent=None).order_by(
            "created_at"
        )

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyCommentAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        post_id = self.kwargs["id"]
        comment_pk = self.kwargs["pk"]

        return Comment.objects.filter(id=comment_pk, article_id=post_id).order_by(
            "created_at"
        )


class RetrieveUpdateDestroyCommentReplyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        post_id = self.kwargs["id"]
        comment_pk = self.kwargs["pk"]

        return Comment.objects.filter(id=comment_pk, article_id=post_id).order_by(
            "created_at"
        )
