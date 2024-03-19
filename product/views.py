from .models import Product, Nutriment, Comment, Vote, Favorite, Category, Allergen, Ingredient
from user.models import User
from user.models import Allergen as UserAllergen
from user.models import DietaryPref as UserIngredient
from file.views import getFile
from suggestion.models import Suggestion
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt


def getAllProducts(request):
    res = []
    for product in Product.objects.order_by("-date"):
        res.append(getProductSer(product))
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


def getProduct(request, id):
    product = Product.objects.get(id = id)
    res = getProductSer(product)
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def createProduct(request):
    data = JSONParser().parse(request)
    product = Product.objects.create(
        code = data["code"],
        name = data["name"],
        brand = data["brand"],
        weight = data["weight"],
        imageUrl = data["imageUrl"]
    )
    product.save()
    for el in data["nutriments"]:
        if (el["value"] == "0"): continue
        nutriment = Nutriment.objects.create(
            productId = product.id,
            name = el["name"],
            unit = el["unit"],
            value = el["value"]
        )
        nutriment.save()
    for el in data["allergens"]:
        allergen = Allergen.objects.create(
            name = el,
            productId = product.id,
        )
        allergen.save()
    for el in data["categories"]:
        category = Category.objects.create(
            name = el,
            productId = product.id,
        )
        category.save()
    for el in data["ingredients"]:
        ingredient = Ingredient.objects.create(
            name = el,
            productId = product.id,
        )
        ingredient.save()
    res = getProductSer(product)
    return JsonResponse(res, status=status.HTTP_201_CREATED, safe=False)


@csrf_exempt
def updateProduct(request, id):
    data = JSONParser().parse(request)
    product = Product.objects.get(id = id)
    product.name = data.get("name", product.name)
    product.brand = data.get("brand", product.brand)
    product.weight = data.get("weight", product.weight)
    product.imageUrl = data.get("imageUrl", product.imageUrl)
    product.save()
    for nutriment in Nutriment.objects.filter(productId = product.id):
        nutriment.delete()
    for allergen in Allergen.objects.filter(productId = product.id):
        allergen.delete()
    for category in Category.objects.filter(productId = product.id):
        category.delete()
    for ingredient in Ingredient.objects.filter(productId = product.id):
        ingredient.delete()
    for el in data["nutriments"]:
        if (el["value"] == "0"): continue
        nutriment = Nutriment.objects.create(
            productId = product.id,
            name = el["name"],
            unit = el["unit"],
            value = el["value"]
        )
        nutriment.save()
    for el in data["allergens"]:
        allergen = Allergen.objects.create(
            productId = product.id,
            name = el,
        )
        allergen.save()
    for el in data["categories"]:
        category = Category.objects.create(
            productId = product.id,
            name = el,
        )
        category.save()
    for el in data["ingredients"]:
        ingredient = Ingredient.objects.create(
            productId = product.id,
            name = el,
        )
        ingredient.save()
    res = getProductSer(product)
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def deleteProduct(request, id):
    product = Product.objects.get(id = id)
    for nutriment in Nutriment.objects.filter(productId = product.id):
        nutriment.delete()
    for allergen in Allergen.objects.filter(productId = product.id):
        allergen.delete()
    for category in Category.objects.filter(productId = product.id):
        category.delete()
    for ingredient in Ingredient.objects.filter(productId = product.id):
        ingredient.delete()
    for comment in Comment.objects.filter(productId = product.id):
        comment.delete()
    for vote in Vote.objects.filter(productId = product.id):
        vote.delete()
    for favorite in Favorite.objects.filter(productId = product.id):
        favorite.delete()
    for suggestion in Suggestion.objects.filter(productId = product.id):
        suggestion.delete()
    product.delete()
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)


def getCommentsByProduct(request, productId):
    res = []
    for comment in Comment.objects.filter(productId = productId, commentId = -1).order_by("-date"):
        res.append(getCommentSer(comment))
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def createComment(request):
    data = JSONParser().parse(request)
    comment = Comment.objects.create(
        productId = data["productId"],
        userId = data["userId"],
        commentId = data.get("commentId", -1),
        content = data["content"]
    )
    comment.save()
    res = getCommentSer(comment)
    return JsonResponse(res, status=status.HTTP_201_CREATED, safe=False)


@csrf_exempt
def updateComment(request, id):
    data = JSONParser().parse(request)
    comment = Comment.objects.get(id = id)
    comment.content = data["content"]
    comment.save()
    res = getCommentSer(comment)
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def deleteComment(request, id):
    comment = Comment.objects.get(id = id)
    for subComment in Comment.objects.filter(commentId = comment.id):
        subComment.delete()
    comment.delete()
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def getFavorites(request, userId):
    res = []
    for favorite in Favorite.objects.filter(userId = userId).order_by("-date"):
        product = Product.objects.get(id = favorite.productId)
        res.append(getProductSer(product))
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def favorite(request):
    data = JSONParser().parse(request)
    favorite, created = Favorite.objects.get_or_create(
        userId = data["userId"],
        productId = data["productId"],
    )
    if created: favorite.save()
    else: favorite.delete()
    res = []
    for favorite in Favorite.objects.filter(productId = data["productId"]):
        res.append(favorite.userId)
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def vote(request):
    data = JSONParser().parse(request)
    votes = Vote.objects.filter(
        productId = data["productId"],
        userId = data["userId"]
    )
    if votes.exists():
        vote = votes[0]
        if vote.up == data["up"]: 
            vote.delete()
        else: 
            vote.up = data["up"]
            vote.save()
    else:
        vote = Vote.objects.create(
            productId = data["productId"],
            userId = data["userId"],
            up = data["up"]
        )
        vote.save()
    res = []
    for vote in Vote.objects.filter(productId = data["productId"]):
        res.append({
            "id": vote.id,
            "userId": vote.userId,
            "up": vote.up
        })
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


def getPrefAllergens(request):
    res = []
    for allergen in Allergen.objects.all():
        if allergen.name not in res:
            res.append(allergen.name)
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)

def getPrefIngredients(request):
    res = []
    for ingredient in Ingredient.objects.all():
        if ingredient.name not in res:
            res.append(ingredient.name)
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


def getPrefCategories(request):
    res = []
    for category in Category.objects.all():
        if category.name not in res:
            res.append(category.name)
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


def getSimilarProducts(request, id):
    PRODUCTS_COUNT = 6
    originProduct = Product.objects.get(id = id)
    products = []
    for brand in originProduct.brand.split(','):
        for product in Product.objects.filter(brand__icontains = brand.strip()):
            if len(products) >= PRODUCTS_COUNT: break
            if product.id not in products and product.id != originProduct.id:
                products.append(product.id)
    for category in Category.objects.filter(productId = originProduct.id):
        for c in Category.objects.filter(name = category.name):
            product = Product.objects.get(id = c.productId)
            if len(products) >= PRODUCTS_COUNT: break
            if product.id not in products and product.id != originProduct.id:
                products.append(product.id)
    res = []
    for productId in products:
        product = Product.objects.get(id = productId)
        res.append(getProductSer(product))
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


def getRecommendations(request, userId):
    PRODUCTS_COUNT = 6
    products = []
    allergens = []
    for allergen in UserAllergen.objects.filter(userId = userId):
        allergens.append(allergen.name)
    for favorite in Favorite.objects.filter(userId = userId):
        originProduct = Product.objects.get(id = favorite.productId)
        for brand in originProduct.brand.split(','):
            for product in Product.objects.filter(brand__icontains = brand.strip()):
                if len(products) >= PRODUCTS_COUNT: break
                productAllergens = []
                for allergen in Allergen.objects.filter(productId = product.id):
                    productAllergens.append(allergen.name)
                if haveCommonElements(allergens, productAllergens): continue
                if product.id not in products and product.id != originProduct.id:
                    products.append(product.id)
        for category in Category.objects.filter(productId = originProduct.id):
            for c in Category.objects.filter(name = category.name):
                if len(products) >= PRODUCTS_COUNT: break
                product = Product.objects.get(id = c.productId)
                productAllergens = []
                for allergen in Allergen.objects.filter(productId = product.id):
                    productAllergens.append(allergen.name)
                if haveCommonElements(allergens, productAllergens): continue
                if product.id not in products and product.id != originProduct.id:
                    products.append(product.id)
    for ingredient in UserIngredient.objects.filter(userId = userId):
        for i in Ingredient.objects.filter(name = ingredient.name):
            if len(products) >= PRODUCTS_COUNT: break
            product = Product.objects.get(id = i.productId)
            productAllergens = []
            for allergen in Allergen.objects.filter(productId = product.id):
                productAllergens.append(allergen.name)
            if haveCommonElements(allergens, productAllergens): continue
            if product.id not in products:
                products.append(product.id)
    res = []
    for productId in products:
        product = Product.objects.get(id = productId)
        res.append(getProductSer(product))
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)
    
    



def getProductSer(product):
    res = {
        "id": product.id,
        "code": product.code,
        "name": product.name,
        "brand": product.brand,
        "weight": product.weight,
        "imageUrl": product.imageUrl,
        "nutriments": [],
        "categories": [],
        "allergens": [],
        "ingredients": [],
        "votes": [],
        "favorites": []
    }
    for nutriment in Nutriment.objects.filter(productId = product.id):
        res["nutriments"].append({
            "id": nutriment.id,
            "name": nutriment.name,
            "unit": nutriment.unit,
            "value": nutriment.value,
        })
    for category in Category.objects.filter(productId = product.id):
        res["categories"].append({
            "id": category.id,
            "name": category.name,
        })
    for allergen in Allergen.objects.filter(productId = product.id):
        res["allergens"].append({
            "id": allergen.id,
            "name": allergen.name,
        })
    for ingredient in Ingredient.objects.filter(productId = product.id):
        res["ingredients"].append({
            "id": ingredient.id,
            "name": ingredient.name,
        })
    for vote in Vote.objects.filter(productId = product.id):
        res["votes"].append({
            "id": vote.id,
            "userId": vote.userId,
            "up": vote.up
        })
    for favorite in Favorite.objects.filter(productId = product.id):
        res["favorites"].append(favorite.userId)
    return res


def getCommentSer(comment):
    user = User.objects.get(id = comment.userId)
    res = {
        "id": comment.id,
        "userId": comment.userId,
        "productId": comment.productId,
        "content": comment.content,
        "date": comment.date,
        "user": {
            "username": user.username,
            "imageUrl": getFile(user.imageId),
        },
        "subComments": []
    }
    for subComment in Comment.objects.filter(commentId = comment.id).order_by("-date"):
        user = User.objects.get(id = comment.userId)
        res["subComments"].append({
            "id": subComment.id,
            "content": subComment.content,
            "date": subComment.date,
            "productId": subComment.productId,
            "userId": subComment.userId,
            "user": {
                "username": user.username,
                "imageUrl": getFile(user.imageId),
            },  
        })
    return res


def haveCommonElements(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)
    intersection = set1.intersection(set2)
    return len(intersection) > 0