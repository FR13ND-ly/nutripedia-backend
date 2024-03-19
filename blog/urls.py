from . import views
from django.urls import path

urlpatterns = [
    path("get/<int:id>/", views.getArtcl),
    path("get/all/", views.getArticles),
    path("create/", views.createArticle),
    path("update/<int:id>/", views.updateArticle),
    path("delete/<int:id>/", views.deleteArticle),

    path("comments/create/", views.createComment),
    path("comments/update/<int:id>/", views.updateComment),
    path("comments/delete/<int:id>/", views.deleteComment),
    path("comments/like/", views.likeComment),
    
    path("like/", views.like),

    path("notifications/get/<int:userId>/last/", views.getLastNotifications),
    path("notifications/get/<int:userId>/all/", views.getAllNotifications),
    path("notifications/seen/<int:userId>/", views.setNotificationSeenAll),
    path("notifications/delete/<int:id>/", views.deleteNotification),
]