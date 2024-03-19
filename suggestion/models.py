from django.db import models
from django.utils import timezone

class Suggestion(models.Model):
    productId = models.PositiveIntegerField()
    userId = models.PositiveIntegerField()
    name = models.TextField()
    brand = models.TextField()
    imageUrl = models.TextField()
    weight = models.TextField()
    state = models.IntegerField(default=-1)
    date = models.DateTimeField(default=timezone.now)


class SuggestionAllergen(models.Model):
    suggestionId = models.PositiveIntegerField()
    name = models.TextField()


class SuggestionCategory(models.Model):
    suggestionId = models.PositiveIntegerField()
    name = models.TextField()
    

class SuggestionIngredient(models.Model):
    suggestionId = models.PositiveIntegerField()
    name = models.TextField()
