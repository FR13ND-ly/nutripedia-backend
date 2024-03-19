from . import views
from django.urls import path

urlpatterns = [
    path("get/waiting/", views.getWaitingSuggestions),
    path("get/by-user/<int:userId>/", views.getSuggestionsByUser),
    path("create/", views.createSuggestion),
    path("update/<int:id>/", views.updateSuggestion),
    path("approve/<int:id>/", views.approveSuggestion),
    path("disapprove/<int:id>/", views.disapproveSuggestion),
    path("delete/<int:id>/", views.deleteSuggestion),
]