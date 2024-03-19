from rest_framework.parsers import JSONParser
from rest_framework import status
from django.http.response import JsonResponse
from .models import Article, Comment, Like, Notification, LikeComment
from file.views import getFile
from user.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


def getArtcl(request, id):
    res = getArticle(Article.objects.get(id = id))
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)

def getArticles(request):
    res = []
    for article in Article.objects.order_by("-date"):
        res.append(getArticle(article))
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def createArticle(request):
    data = JSONParser().parse(request)
    article = Article.objects.create(
        content = data["content"],
        userId = data["userId"]
    )
    article.save()
    res = getArticle(article)
    return JsonResponse(res, status=status.HTTP_201_CREATED, safe=False)


@csrf_exempt
def updateArticle(request, id):
    data = JSONParser().parse(request)
    article = Article.objects.get(id = id)
    article.content = data["content"]
    article.edited = True
    article.date = timezone.now()
    article.save()
    res = getArticle(article)
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def deleteArticle(request, id):
    article = Article.objects.get(id = id)
    for comment in Comment.objects.filter(articleId = article.id):
        comment.delete()
    for like in Like.objects.filter(articleId = article.id):
        like.delete()
    article.delete()
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def createComment(request):
    data = JSONParser().parse(request)
    comment = Comment.objects.create(
        articleId = data["articleId"],
        userId = data["userId"],
        commentId = data.get("commentId", -1),
        content = data["content"]
    )
    comment.save()
    res = getComment(comment)
    receiverId = Article.objects.get(id = comment.articleId).userId
    addNotification(comment.articleId, comment.userId, receiverId, "added a comment to your article")
    return JsonResponse(res, status=status.HTTP_201_CREATED, safe=False)


@csrf_exempt
def updateComment(request, id):
    data = JSONParser().parse(request)
    comment = Comment.objects.get(id = id)
    comment.content = data["content"]
    comment.save()
    res = getComment(comment)
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def deleteComment(request, id):
    comment = Comment.objects.get(id = id)
    for subComment in Comment.objects.filter(commentId = comment.id):
        subComment.delete()
    comment.delete()
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def like(request):
    data = JSONParser().parse(request)
    like, created = Like.objects.get_or_create(articleId = data["articleId"], userId = data["userId"])
    if created: 
        like.save()
        receiverId = Article.objects.get(id = like.articleId).userId
        addNotification(like.articleId, like.userId, receiverId, "liked your article")
    else: like.delete()
    likes = []
    for like in Like.objects.filter(articleId = like.articleId):
        likes.append({
            "id": like.id,
            "userId": like.userId,
        })
    return JsonResponse(likes, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def likeComment(request):
    data = JSONParser().parse(request)
    like, created = LikeComment.objects.get_or_create(commentId = data["commentId"], userId = data["userId"])
    if created: 
        like.save()
        article = Article.objects.get(id = Comment.objects.get(id = like.commentId).articleId)
        addNotification(article.id, like.userId, article.userId, "liked your comment")
    else: like.delete()
    likes = []
    for like in LikeComment.objects.filter(commentId = like.commentId):
        likes.append({
            "id": like.id,
            "userId": like.userId,
        })
    return JsonResponse(likes, status=status.HTTP_200_OK, safe=False)


def getLastNotifications(request, userId):
    res = {
        "userId": userId,
        "unseen": Notification.objects.filter(userId = userId, seen = False).count(),
        "last": []
    }
    for notification in Notification.objects.filter(userId = userId).order_by("-date")[:3]:
        res["last"].append(getNotification(notification))
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


def getAllNotifications(request, userId):
    res = []
    for notification in Notification.objects.filter(userId = userId).order_by("-date"):
        res.append(getNotification(notification))
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def createNotification(request):
    data = JSONParser().parse(request)
    notification = Notification.objects.create(
        userId = data["userId"],
        articleId = data["articleId"],
        content = data["content"],
    )
    notification.save()
    return JsonResponse(getNotification(notification), status=status.HTTP_201_CREATED, safe=False)


def setNotificationSeenAll(request, userId):
    for notification in Notification.objects.filter(userId = userId):
        notification.seen = True
        notification.save()
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def deleteNotification(request, id):
    notification = Notification.objects.get(id = id)
    notification.delete()
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)


def getNotification(notification):
    return {
        "id": notification.id,
        "articleId": notification.articleId,
        "content": notification.content,
        "seen": notification.seen,
        "date": notification.date,
    }


def getComment(comment):
    user = User.objects.get(id = comment.userId)
    res = {
        "id": comment.id,
        "userId": comment.userId,
        "articleId": comment.articleId,
        "content": comment.content,
        "user": {
            "username": user.username,
            "imageUrl": getFile(user.imageId),
        },
        "subComments": [],
        "likes": [],
        "date": comment.date
    }
    for like in LikeComment.objects.filter(commentId = comment.id):
        res["likes"].append({
            "userId": like.userId
        })
    for subComment in Comment.objects.filter(commentId = comment.id).order_by("-date"):
        user = User.objects.get(id = comment.userId)
        sc = {
            "id": subComment.id,
            "userId": comment.userId,
            "articleId": comment.articleId,
            "content": subComment.content,
            "user": {
                "username": user.username,
                "imageUrl": getFile(user.imageId),
            },          
            "likes": [],
            "date": comment.date
        }
        for like in LikeComment.objects.filter(commentId = subComment.id):
            sc["likes"].append({
                "userId": like.userId
            })
        res["subComments"].append(sc)
    return res


def getArticle(article):
    user = User.objects.get(id = article.userId)
    res = {
        "id": article.id,
        "content": article.content,
        "user": {
            "id": user.id,
            "username": user.username,
            "imageUrl": getFile(user.imageId),
        },
        "likes": [],
        "comments": [],
        "date": article.date
    }
    for comment in Comment.objects.filter(articleId = article.id, commentId = -1).order_by("-date"):
        res["comments"].append(getComment(comment))
    for like in Like.objects.filter(articleId = article.id):
        res["likes"].append({
            "id": like.id,
            "userId": like.userId,
        })
    return res

def addNotification(articleId, userId, receiverId, content):
    if userId == receiverId: return
    user = User.objects.get(id = userId)
    notification = Notification.objects.create(
        articleId = articleId,
        userId = receiverId,
        content = f"{ user.username } { content }"
    )
    notification.save()
    return