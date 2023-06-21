from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .controller import views_control,logic
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def busqueda_contenido(request):
    retornos = views_control().buscar_contenido_por_texto(logic().extraccion_atributos_en_objeto(request.POST) )
    return HttpResponse (
		json.dumps({"retorno":"ok","data":retornos}),
		content_type = "application/json"
	)

@csrf_exempt
def recomendacion_home(request):
    retornos = views_control().recomendar_contenido_home(logic().extraccion_atributos_en_objeto(request.POST) )
    return HttpResponse (
		json.dumps({"retorno":"ok","data":retornos}),
		content_type = "application/json"
	)
@csrf_exempt
def recomendacion_video(request):
    retornos = views_control().recomendar_contenido_video(logic().extraccion_atributos_en_objeto(request.POST) )
    return HttpResponse (
		json.dumps({"retorno":"ok","data":retornos}),
		content_type = "application/json"
	)
@csrf_exempt
def view_crear_usuario(request):
    retornos = views_control().crear_usuario( logic().extraccion_atributos_en_objeto(request.POST) )
    return HttpResponse (
		json.dumps({"retorno":retornos}),
		content_type = "application/json"
	)
@csrf_exempt
def view_crear_contenido(request):
    retornos = views_control().crear_contenido( logic().extraccion_atributos_en_objeto(request.POST) )
    return HttpResponse (
		json.dumps({"retorno":retornos}),
		content_type = "application/json"
	)
@csrf_exempt
def view_crear_relations(request):
    retornos = views_control().crear_relations( logic().extraccion_atributos_en_objeto(request.POST) )
    return HttpResponse (
		json.dumps({"retorno":retornos}),
		content_type = "application/json"
	)

@csrf_exempt
def view_crear_consumo(request):
    retornos = views_control().crear_consumo(logic().extraccion_atributos_en_objeto(request.POST) )
    return HttpResponse (
		json.dumps({"retorno":retornos}),
		content_type = "application/json"
	)
def health(request):
    return HttpResponse("Healthy nutra.")



