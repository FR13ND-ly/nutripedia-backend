from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=64, unique=True)
    password = models.TextField()
    isAdmin = models.BooleanField(default=False)
    imageId = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(default=timezone.now)


class Token(models.Model):
    userId = models.PositiveIntegerField()
    token = models.TextField()
    date = models.DateTimeField(default=timezone.now)


class DietaryPref(models.Model):
    userId = models.PositiveIntegerField()
    name = models.TextField()

    def __str__(self) -> str:
        return self.name + " " + User.objects.get(id = self.userId).username


class Allergen(models.Model):
    userId = models.PositiveIntegerField()
    name = models.TextField()

    def __str__(self) -> str:
        return self.name + " " + User.objects.get(id = self.userId).username