from . import views
from django.urls import path

urlpatterns = [
    path("get/all/", views.getAllProducts),
    path("get/<int:id>/", views.getProduct),
    path("create/", views.createProduct),
    path("update/<int:id>/", views.updateProduct),
    path("delete/<int:id>/", views.deleteProduct),
    path("similar/<int:id>/", views.getSimilarProducts),
    path("recommendations/<int:userId>/", views.getRecommendations),

    path("comments/get/<int:productId>/", views.getCommentsByProduct),
    path("comments/create/", views.createComment),
    path("comments/update/<int:id>/", views.updateComment),
    path("comments/delete/<int:id>/", views.deleteComment),

    path("prefs/allergens/", views.getPrefAllergens),
    path("prefs/ingredients/", views.getPrefIngredients),
    path("prefs/categories/", views.getPrefCategories),
    path("vote/", views.vote),
    path("favorite/", views.favorite),
    path("favorite/get/<int:userId>/", views.getFavorites),
    
]