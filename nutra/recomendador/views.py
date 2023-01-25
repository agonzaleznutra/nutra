from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from pymongo import MongoClient
import urllib.parse
import datetime
def extraccion_atributos_en_objeto(obj):
    
    res = {}
    for o in obj:
        if o != "_id":
            if ".json" in o:
                print(o)
                res[o.split(".json")[0].strip()]  = json.loads(obj[o])
            elif "[]" in o:
                lista = obj.getlist(o, [])
                if len(lista) == 1 and lista[0].strip() == '':
                    lista = []
                nwlista = []
                for j in lista:
                    try:
                        nwlista.append(json.loads(j))
                    except:
                        nwlista.append(j.strip())
                res[o.split("[]")[0].strip()] = nwlista
            else:
                if o == "id" and obj[o]== "null":
                    res[o] = ""
                else:
                    res[o.strip()] = obj[o].strip()
    
    res["fecha"] = datetime.datetime.now().strftime("%Y-%m-%d")
    return res
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
def filtrado(obj):
    username = urllib.parse.quote_plus('aleja_user')
    password = urllib.parse.quote_plus('02-10-91aldigovE')

    mongo_client = MongoClient(str("mongodb://%s:%s@172.31.22.3") % (username, password))
    salida = mongo_client.nutra.contenidos.find()
    retornos = {"tendencia":[],"recomendacion":[],"volveraver":[]}
    for o in salida:
        retornos["tendencia"].append(o["id_contenido"])
        retornos["recomendacion"].append(o["id_contenido"])
        retornos["volveraver"].append(o["id_contenido"])
    return retornos
@csrf_exempt
def recomendacion(request):
    print("recomendacion---",request.POST)
    obj = extraccion_atributos_en_objeto(request.POST) 
    salida = filtrado(obj)

    return HttpResponse (
		json.dumps({"retorno":"ok","data":salida}),
		content_type = "application/json"
	)
@csrf_exempt
def load_content(request):
    salida = extraccion_atributos_en_objeto(request.POST) 
    
    username = urllib.parse.quote_plus('aleja_user')
    password = urllib.parse.quote_plus('02-10-91aldigovE')

    mongo_client = MongoClient(str("mongodb://%s:%s@172.31.22.3") % (username, password))

    id = mongo_client.nutra.contenidos.find_one({"id_contenido":salida["id_contenido"]})
    if id is None:
        mongo_client.nutra.contenidos.insert_one(salida)
    else:
        mongo_client.nutra.contenidos.update_one({"id_contenido":salida["id_contenido"]},{"$set":salida})
    return HttpResponse (
		json.dumps({"retorno":"ok"}),
		content_type = "application/json"
	)
@csrf_exempt
def set_consumo(request):
    salida = extraccion_atributos_en_objeto(request.POST) 
    username = urllib.parse.quote_plus('aleja_user')
    password = urllib.parse.quote_plus('02-10-91aldigovE')
    mongo_client = MongoClient(str("mongodb://%s:%s@172.31.22.3") % (username, password))
    mongo_client.nutra.consumos.insert_one(salida)
    print("....insercion consumo...",salida)
    return HttpResponse (
		json.dumps({"retorno":"ok"}),
		content_type = "application/json"
	)
def health(request):
    return HttpResponse("Healthy nutra.")



