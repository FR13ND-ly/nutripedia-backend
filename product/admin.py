from django.contrib import admin
from .models import Product, Comment, Vote, Favorite

admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Favorite)