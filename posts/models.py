from django.db import models


class Post(models.Model):
    creator = models.CharField(max_length=50, default="me")
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50, verbose_name="Name")
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField()
    votes = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class CommentQuerySet(models.QuerySet):
    def for_post(self, post_id):
        return self.filter(article_id=post_id)

    def roots(self):
        return self.filter(parent__isnull=True)

    def ordered(self):
        return self.order_by("created_at")


class Comment(models.Model):
    article = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name="Posts", related_name="comments"
    )
    author = models.CharField(max_length=50, verbose_name="Name")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    objects = CommentQuerySet.as_manager()

    def children(self):
        return self.__class__.objects.filter(parent_id=self.pk)

    @property
    def is_parent(self):
        return self.parent is None

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-created_at"]
