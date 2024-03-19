from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import File
from django.conf import settings
from rest_framework import status
import os 

@csrf_exempt
def addFile(request):
    file = File.objects.create(file=request.FILES['file'])
    file.save()
    return JsonResponse(file.id, status=status.HTTP_200_OK, safe=False)


def getFile(id, path=""):
    files = File.objects.filter(id=id)
    if files.exists():
        return settings.API_URL + "media/" + path + os.path.basename(files[0].file.name)
    else:
        return ""