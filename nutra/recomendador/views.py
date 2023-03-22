from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from pymongo import MongoClient
import urllib.parse
import datetime
username = urllib.parse.quote_plus('aleja_user')
password = urllib.parse.quote_plus('02-10-91aldigovE')
def mc():
    return MongoClient(str("mongodb://%s:%s@172.31.22.3") % (username, password))
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
    #LOGICA PENDIENTE CON SISTEMA DE RECOMENDACIÓN
    
    salida = mc().nutra.contenidos.find({})
    retornos = {"tendencia":[],"recomendacion":[],"volveraver":[]}
    for o in salida:
        retornos["tendencia"].append(int(o["id_contenido"]))
        retornos["recomendacion"].append(int(o["id_contenido"]))
        retornos["volveraver"].append(int(o["id_contenido"]))
    """
    retornos["tendencia"] = [2,3,4,5]
    retornos["recomendacion"] = [6,7,8,9]
    retornos["volveraver"] = [10,11,12,13]
    """
    return retornos
@csrf_exempt
def filter(request):
    campos = ["titulo","resumen","productos1","productos2","productos3","productos4","keyword1","keyword2","keyword3","keyword4","busqueda1","busqueda2","busqueda3"]
    obj = extraccion_atributos_en_objeto(request.POST) 
    tmp = mc().nutra.contenidos.find()
    retornos= {"filtrado":[]}
    for o in tmp:
        consolidado = ""
        for c in campos:
            if c in o:
                consolidado = consolidado + o[c]+" "
        #consolidado = o["titulo"]+" "+o["resumen"]+" "+o["productos1"]+" "+o["productos2"]+" "+o["productos3"]+" "+o["productos4"]+" "+o["keyword1"]+" "+o["keyword2"]+" "+o["keyword3"]+" "+o["keyword4"]+" "+o["busqueda1"]+" "+o["busqueda2"]+" "+o["busqueda3"]
        print(o)
        for q in obj["query"].split(" "):
            if q.lower() in consolidado.lower():
                retornos["filtrado"].append(int(o["id_contenido"]))
    
    
    return HttpResponse (
		json.dumps({"retorno":"ok","data":retornos}),
		content_type = "application/json"
	)

@csrf_exempt
def recomendacion(request):
    
    obj = extraccion_atributos_en_objeto(request.POST) 
    salida = filtrado(obj)
    print("recomendacion---",request.POST,salida)
    return HttpResponse (
		json.dumps({"retorno":"ok","data":salida}),
		content_type = "application/json"
	)
@csrf_exempt
def load_content(request):
    salida = extraccion_atributos_en_objeto(request.POST) 
    
    mc = mc()

    id = mc.nutra.contenidos.find_one({"id_contenido":salida["id_contenido"]})
    if id is None:
        mc.nutra.contenidos.insert_one(salida)
    else:
        mc.nutra.contenidos.update_one({"id_contenido":salida["id_contenido"]},{"$set":salida})
    return HttpResponse (
		json.dumps({"retorno":"ok"}),
		content_type = "application/json"
	)
@csrf_exempt
def set_consumo(request):
    salida = extraccion_atributos_en_objeto(request.POST) 
    
    mc().nutra.consumos.insert_one(salida)
    print("....insercion consumo...",salida)
    return HttpResponse (
		json.dumps({"retorno":"ok"}),
		content_type = "application/json"
	)
def health(request):
    return HttpResponse("Healthy nutra.")



