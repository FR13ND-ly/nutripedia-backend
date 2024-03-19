from django.contrib import admin
from .models import User, Allergen, DietaryPref

admin.site.register(User)
admin.site.register(Allergen)
admin.site.register(DietaryPref)