from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
@csrf_exempt
def recomendacion(request):
    print("controladooo alvaro",request.POST,request.GET)
    retorno = {"s1":request.POST.get('cat1', 'No data found'),
    "s2":request.POST.get('cat2', 'No data found'),
    "s3":request.POST.get('cat3', 'No data found'),
    "s4":request.POST.get('cat4', 'No data found')}
    return HttpResponse (
		json.dumps(retorno),
		content_type = "application/json"
	)	
def health(request):
    return HttpResponse("Healthy nutra.")