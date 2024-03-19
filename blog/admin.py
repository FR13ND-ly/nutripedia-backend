from django.contrib import admin
from .models import Article, Comment, Like, Notification

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Notification)