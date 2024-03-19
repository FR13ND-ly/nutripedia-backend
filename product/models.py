from django.db import models
from django.utils import timezone


class Product(models.Model):
    code = models.TextField()
    name = models.TextField()
    brand = models.TextField()
    imageUrl = models.TextField()
    weight = models.TextField()
    date = models.DateTimeField(default=timezone.now)


class Nutriment(models.Model):
    productId = models.PositiveIntegerField()
    name = models.TextField()
    unit = models.TextField()
    value = models.PositiveIntegerField()


class Allergen(models.Model):
    productId = models.PositiveIntegerField()
    name = models.TextField()


class Category(models.Model):
    productId = models.PositiveIntegerField()
    name = models.TextField()


class Ingredient(models.Model):
    productId = models.PositiveIntegerField()
    name = models.TextField()


class Comment(models.Model):
    productId = models.PositiveIntegerField()
    userId = models.PositiveIntegerField()
    commentId = models.IntegerField(default=-1)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content
    

class Vote(models.Model):
    productId = models.PositiveIntegerField()
    userId = models.PositiveIntegerField()
    up = models.BooleanField(null=False)
    date = models.DateTimeField(default=timezone.now)


class Favorite(models.Model):
    userId = models.PositiveIntegerField()
    productId = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)