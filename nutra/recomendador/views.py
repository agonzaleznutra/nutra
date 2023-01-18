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
    "s2":request.GET.get('cat2', 'No data found'),
    "s3":request.GET.get('cat3', 'No data found'),
    "s4":request.GET.get('cat4', 'No data found')}
    return HttpResponse (
		json.dumps(retorno),
		content_type = "application/json"
	)	
@csrf_exempt
def load_content(request):
    print("controladooo alvaro222",request.body,request.POST)
    
    return HttpResponse (
		json.dumps({"retorno":"ok"}),
		content_type = "application/json"
	)
def health(request):
    return HttpResponse("Healthy nutra.")



