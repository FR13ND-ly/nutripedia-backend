from . import views
from django.urls import path

urlpatterns = [
    path("files/add/", views.addFile),
]