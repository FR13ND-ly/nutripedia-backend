from django.contrib import admin
from .models import Suggestion, SuggestionAllergen, SuggestionCategory, SuggestionIngredient

admin.site.register(Suggestion)
admin.site.register(SuggestionAllergen)
admin.site.register(SuggestionCategory)
admin.site.register(SuggestionIngredient)