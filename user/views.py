from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import User, Token, DietaryPref, Allergen
from django.contrib.auth.hashers import make_password, verify_password
from file.views import getFile
import secrets
import string
import g4f

@csrf_exempt
def authentificate(request):
    data = JSONParser().parse(request)
    user = User.objects.filter(username = data["username"])
    res = {
        "message": "Incorrect username",
        "logged": False,
    }
    if (not user.exists()): return JsonResponse(res, status=status.HTTP_401_UNAUTHORIZED, safe=False)
    user = user[0   ]
    if (verify_password(data["password"], user.password)[0]):
        token = Token.objects.create(
            userId = user.id,
            token = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(15))
        )        
        token.save()
        res = {
            "id": user.id,
            "logged": True,
            "username": user.username,
            "isAdmin": user.isAdmin,
            "token": token.token,
            "imageUrl": getFile(user.imageId)
        }
    else: 
        res = {
            "message": "Incorrect password",
            "logged": False,
        }
        return JsonResponse(res, status=status.HTTP_401_UNAUTHORIZED, safe=False)
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


def authorization(request, token):
    token = Token.objects.filter(token=token)
    if (token.exists()):
        user = User.objects.get(id = token[0].userId)        
        res = {
            "id": user.id,
            "logged": True,
            "username": user.username,
            "isAdmin": user.isAdmin,
            "token": token[0].token,
            "imageUrl": getFile(user.imageId)
        }
    else :
        res = { "logged": False }
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def setPreferences(request, id):
    data = JSONParser().parse(request)
    user = User.objects.get(id = id)
    for allergen in Allergen.objects.filter(userId = user.id):
        allergen.delete()
    for dietaryPref in DietaryPref.objects.filter(userId = user.id):
        dietaryPref.delete()
    for allergen in data["allergens"]:
        allergen = Allergen.objects.create(
            name = allergen,
            userId = user.id
        )
        allergen.save()
    for dietaryPref in data["dietaryPrefs"]:
        dietaryPref = DietaryPref.objects.create(
            name = dietaryPref,
            userId = user.id
        )
        dietaryPref.save()
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def register(request):
    data = JSONParser().parse(request)
    if User.objects.filter(username=data["username"]).exists():
        return JsonResponse({
            "message": "Username already taken"
        }, status=status.HTTP_409_CONFLICT, safe=False)
    user = User.objects.create(
        username = data["username"],
        password = make_password(data["password"])
    )
    user.save()
    token = Token.objects.create(
        userId = user.id,
        token = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(15))
    ) 
    res = {
        "id": user.id,
        "logged": True,
        "username": user.username,
        "isAdmin": user.isAdmin,
        "token": token.token,
        "imageUrl": getFile(user.imageId)
    }
    return JsonResponse(res, status=status.HTTP_201_CREATED, safe=False)


def getUser(request, id):
    user = User.objects.get(id = id)
    res = {
        "id": user.id,
        "username": user.username,
        "imageUrl": getFile(user.imageId),
        'allergens': [],
        'dietaryPrefs': []
    }
    for allergen in Allergen.objects.filter(userId = user.id):
        res["allergens"].append(allergen.name)
    for dietaryPref in DietaryPref.objects.filter(userId = user.id):
        res["dietaryPrefs"].append(dietaryPref.name)
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def updateUser(request, id):
    data = JSONParser().parse(request)
    user = User.objects.get(id = id)
    user.imageId = data.get("imageId", user.imageId)
    user.save()
    res = getFile(user.imageId),
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
def ai(request):
    data = JSONParser().parse(request)
    allergens = []
    dietaryPrefs = []
    for allergen in Allergen.objects.filter(userId = data["userId"]):
        allergens.append(allergen.name)
    for dietaryPref in DietaryPref.objects.filter(userId = data["userId"]):
        dietaryPrefs.append(dietaryPref.name)
    question = data["question"]
    allergensString = ' '.join(el for el in allergens)
    dietaryPrefsString = ' '.join(el for el in dietaryPrefs)
    query = f"I have this allergens: {allergensString}; and next dietary preferences: {dietaryPrefsString}. {question}"
    res = g4f.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": query}],
    )
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)