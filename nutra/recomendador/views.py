from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from pymongo import MongoClient
import urllib.parse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
@csrf_exempt
def recomendacion(request):
    print(request.POST)
    
    return HttpResponse (
		json.dumps({"retorno":"ok"}),
		content_type = "application/json"
	)
@csrf_exempt
def load_content(request):
    print(request.POST)
    
    username = urllib.parse.quote_plus('aleja_user')
    password = urllib.parse.quote_plus('02-10-91aldigovE')

    mongo_client = MongoClient(str("127.0.0.1") % (username, password))
    mongo_client.contenidos.insert_one(request.POST)
    return HttpResponse (
		json.dumps({"retorno":"ok"}),
		content_type = "application/json"
	)
def health(request):
    return HttpResponse("Healthy nutra.")



