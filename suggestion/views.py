from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Suggestion, SuggestionAllergen, SuggestionCategory, SuggestionIngredient
from product.models import Product, Allergen, Category, Ingredient
from user.models import User
from rest_framework import status
from file.views import getFile


def getWaitingSuggestions(request):
    res = []
    for suggestion in Suggestion.objects.filter(state=-1).order_by("-date"):
        res.append(getSuggestion(suggestion))
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


def getSuggestionsByUser(request, userId):
    res = []
    for suggestion in Suggestion.objects.filter(userId = userId).order_by("-date"):
        res.append(getSuggestion(suggestion))
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def createSuggestion(request):
    data = JSONParser().parse(request)
    suggestion = Suggestion.objects.create(
        productId = data["productId"],
        userId = data["userId"],
        name = data["name"],
        brand = data["brand"],
        weight = data["weight"],
        imageUrl = data["imageUrl"]
    )
    suggestion.save()
    for el in data["allergens"]:
        allergen = SuggestionAllergen.objects.create(
            suggestionId = suggestion.id,
            name = el,
        )
        allergen.save()
    for el in data["categories"]:
        category = SuggestionCategory.objects.create(
            suggestionId = suggestion.id,
            name = el,
        )
        category.save()
    for el in data["ingredients"]:
        ingredient = SuggestionIngredient.objects.create(
            suggestionId = suggestion.id,
            name = el
        )
        ingredient.save()
    res = getSuggestion(suggestion)
    return JsonResponse(res, status=status.HTTP_201_CREATED, safe=False)

@csrf_exempt
def updateSuggestion(request, id):
    data = JSONParser().parse(request)
    suggestion = Suggestion.objects.get(id = id)
    suggestion.name = data.get("name", suggestion.name)
    suggestion.brand = data.get("brand", suggestion.brand)
    suggestion.weight = data.get("weight", suggestion.weight)
    suggestion.imageUrl = data.get("imageUrl", suggestion.imageUrl)
    suggestion.save()
    for allergen in SuggestionAllergen.objects.filter(suggestionId = suggestion.id):
        allergen.delete()
    for category in SuggestionCategory.objects.filter(suggestionId = suggestion.id):
        category.delete()
    for ingredient in SuggestionIngredient.objects.filter(suggestionId = suggestion.id):
        ingredient.delete()
    for el in data["allergens"]:
        allergen = SuggestionAllergen.objects.create(
            suggestionId = suggestion.id,
            name = el,
        )
        allergen.save()
    for el in data["categories"]:
        category = SuggestionCategory.objects.create(
            suggestionId = suggestion.id,
            name = el,
        )
        category.save()
    for el in data["ingredients"]:
        ingredient = SuggestionIngredient.objects.create(
            suggestionId = suggestion.id,
            name = el,
        )
        ingredient.save()
    res = getSuggestion(suggestion)
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


def approveSuggestion(request, id):
    suggestion = Suggestion.objects.get(id = id)
    suggestion.state = 1
    suggestion.save()
    applySuggestion(suggestion)
    res = getSuggestion(suggestion)
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


def disapproveSuggestion(request, id):
    suggestion = Suggestion.objects.get(id = id)
    suggestion.state = 0
    suggestion.save()
    res = getSuggestion(suggestion)
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def deleteSuggestion(request, id):
    suggestion = Suggestion.objects.get(id = id)
    for allergen in SuggestionAllergen.objects.filter(suggestionId = suggestion.id):
        allergen.delete()
    for category in SuggestionCategory.objects.filter(suggestionId = suggestion.id):
        category.delete()
    for ingredient in SuggestionIngredient.objects.filter(suggestionId = suggestion.id):
        ingredient.delete()
    suggestion.delete()
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)


def getSuggestion(suggestion):
    product = Product.objects.get(id = suggestion.productId)
    user = User.objects.get(id = suggestion.userId)
    res = {
        "id": suggestion.id,
        "code": product.code,
        "state": suggestion.state,
        "date": suggestion.date,
        "user": {
            "id": user.id,
            "username": user.username,
            "imageUrl": getFile(user.imageId)
        },
        "name": {
            "new": suggestion.name,
            "old": product.name,
        },
        "brand": {
            "new": suggestion.brand,
            "old": product.brand,
        },
        "weight": {
            "new": suggestion.weight,
            "old": product.weight,
        },
        "imageUrl": {
            "new": suggestion.imageUrl,
            "old": product.imageUrl,
        },
        "categories": {
            "new": [],
            "old": []
        },
        "allergens": {
            "new": [],
            "old": []
        },
        "ingredients": {
            "new": [],
            "old": []
        }
    }
    for category in Category.objects.filter(productId = product.id):
        res["categories"]["old"].append({
            "id": category.id,
            "name": category.name,
        })
    for category in SuggestionCategory.objects.filter(suggestionId = suggestion.id):
        res["categories"]["new"].append({
            "id": category.id,
            "name": category.name,
        })
    for allergen in Allergen.objects.filter(productId = product.id):
        res["allergens"]["old"].append({
            "id": allergen.id,
            "name": allergen.name,
        })
    for allergen in SuggestionAllergen.objects.filter(suggestionId = suggestion.id):
        res["allergens"]["new"].append({
            "id": allergen.id,
            "name": allergen.name,
        })
    for ingredient in Ingredient.objects.filter(productId = product.id):
        res["ingredients"]["old"].append({
            "id": ingredient.id,
            "name": ingredient.name,
        })
    for ingredient in SuggestionIngredient.objects.filter(suggestionId = suggestion.id):
        res["ingredients"]["new"].append({
            "id": ingredient.id,
            "name": ingredient.name,
        })
    return res


def applySuggestion(suggestion):
    product = Product.objects.get(id = suggestion.productId)
    product.name = suggestion.name
    product.brand = suggestion.brand
    product.weight = suggestion.weight
    product.imageUrl = suggestion.imageUrl
    product.save()
    for allergen in Allergen.objects.filter(productId = product.id):
        allergen.delete()
    for category in Category.objects.filter(productId = product.id):
        category.delete()
    for ingredient in Ingredient.objects.filter(productId = product.id):
        ingredient.delete()
    for el in SuggestionAllergen.objects.filter(suggestionId = suggestion.id):
        allergen = Allergen.objects.create(
            productId = product.id,
            name = el.name,
        )
        allergen.save()
    for el in SuggestionCategory.objects.filter(suggestionId = suggestion.id):
        category = Category.objects.create(
            productId = product.id,
            name = el.name,
        )
        category.save()
    for el in SuggestionIngredient.objects.filter(suggestionId = suggestion.id):
        ingredient = Ingredient.objects.create(
            productId = product.id,
            name = el.name,
        )
        ingredient.save()

def checkRepeat(suggestion):
    REQUIRED_REPEATS = 5
    return