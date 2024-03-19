from . import views
from django.urls import path

urlpatterns = [
    path("register/", views.register),
    path("authentification/", views.authentificate),
    path("authorization/<str:token>/", views.authorization),

    path("get/<int:id>/", views.getUser),
    path("update/<int:id>/", views.updateUser),

    path("preferences/set/<int:id>/", views.setPreferences),
    path("ai/", views.ai),

]