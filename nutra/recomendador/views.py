from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .controller import extraccion_atributos_en_objeto,buscar_contenido_por_texto,recomendar_contenido_home,crear_contenido,crear_consumo

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def busqueda_contenido(request):
    retornos = buscar_contenido_por_texto(extraccion_atributos_en_objeto(request.POST) )
    return HttpResponse (
		json.dumps({"retorno":"ok","data":retornos}),
		content_type = "application/json"
	)

@csrf_exempt
def recomendacion_home(request):
    retornos = recomendar_contenido_home(extraccion_atributos_en_objeto(request.POST) )
    return HttpResponse (
		json.dumps({"retorno":"ok","data":retornos}),
		content_type = "application/json"
	)
@csrf_exempt
def view_crear_contenido(request):
    retornos = crear_contenido( extraccion_atributos_en_objeto(request.POST) )
    return HttpResponse (
		json.dumps({"retorno":retornos}),
		content_type = "application/json"
	)
@csrf_exempt
def view_crear_consumo(request):
    retornos = crear_consumo(extraccion_atributos_en_objeto(request.POST) )
    return HttpResponse (
		json.dumps({"retorno":retornos}),
		content_type = "application/json"
	)
def health(request):
    return HttpResponse("Healthy nutra.")



