# posts/serializers.py
from rest_framework import serializers
from . import models


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("title", "author", "link", "created_at", "votes", "comments")
        model = models.Post


class CommentSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()

    class Meta:
        fields = ("content", "created_at", "author", "article", "reply_count")
        model = models.Comment

    def get_reply_count(self, obj):
        return obj.children().count() if obj.is_parent else 0


class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("content", "created_at", "author", "parent")
        model = models.Comment


class CommentDetailSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        fields = ("content", "created_at", "author", "parent", "replies")
        model = models.Comment

    def get_replies(self, obj):
        return (
            CommentSerializer(
                obj.children(), many=True).data if obj.is_parent else None
        )
