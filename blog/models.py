from django.db import models
from django.utils import timezone


class Article(models.Model):
    userId = models.PositiveIntegerField()
    content = models.TextField()
    edited = models.BooleanField(default = False)
    date = models.DateTimeField(default=timezone.now)


class Comment(models.Model):
    articleId = models.PositiveIntegerField()
    userId = models.PositiveIntegerField()
    commentId = models.IntegerField(default=-1)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content
    

class Like(models.Model):
    articleId = models.PositiveIntegerField()
    userId = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)


class LikeComment(models.Model):
    commentId = models.PositiveIntegerField()
    userId = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)


class Notification(models.Model):
    userId = models.PositiveIntegerField()
    articleId = models.PositiveIntegerField()
    content = models.TextField()
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
