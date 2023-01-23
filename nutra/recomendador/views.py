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
@csrf_exempt
def recomendacion(request):
    print(request.POST)
    
    return HttpResponse (
		json.dumps({"retorno":"ok"}),
		content_type = "application/json"
	)
@csrf_exempt
def load_content(request):
    salida = extraccion_atributos_en_objeto(request.POST)
    
    username = urllib.parse.quote_plus('aleja_user')
    password = urllib.parse.quote_plus('02-10-91aldigovE')

    mongo_client = MongoClient(str("mongodb://%s:%s@127.0.0.1") % (username, password))

    id = mongo_client.nutra.contenidos.find_one({"id_contenido":salida["id_contenido"]})
    if id is None:
        mongo_client.nutra.contenidos.insert_one(salida)
    else:
        mongo_client.nutra.contenidos.update_one({"id_contenido":salida["id_contenido"]},{"$set":salida})
    return HttpResponse (
		json.dumps({"retorno":"ok"}),
		content_type = "application/json"
	)
def health(request):
    return HttpResponse("Healthy nutra.")



