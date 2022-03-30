from django.db import models


class Post(models.Model):
    creator = models.CharField(max_length=50, default='me')
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50, verbose_name="Name")
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField()
    votes = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class Comment(models.Model):
    article = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name="Posts", related_name="comments"
    )
    author = models.CharField(max_length=50, verbose_name="Name")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        return self.parent is None

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-created_at"]
