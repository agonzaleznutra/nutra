from string import punctuation
non_words = list(punctuation)
from nltk.corpus import stopwords
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from .model import crud
import datetime

language_stopwords = stopwords.words('spanish')
#los tipos de consulta define consultas que validan contra varios campos un valor y son predefinidas
tipos = {
    "todos" : ["titulo","presentador","resumen",
              "productos1","productos2","productos3","productos4",
              "productos5","productos6","productos7","productos8",
              "productos9","productos10","productos11","productos12","productos13","productos14","productos15","productos16","productos17",
              "keyword1","keyword2","keyword3","keyword4","keyword5","keyword6",
              "keyword_diagnostico","contenido_orientacion4",
              "busqueda1","busqueda2","busqueda3",
              "cincor",
              "solo_medicos1","solo_medicos2","solo_medicos3","solo_medicos4","medicos_profesionales1",
              "medicos_profesionales2","medicos_profesionales3","medicos_profesionales4","pacientes","pacientes2",
              "tema_solo_medicos1","tema_solo_medicos2","tema_solo_medicos3","tema_solo_medicos4","tema_medicos_profesionales1",
              "tema_medicos_profesionales2","tema_medicos_profesionales3","tema_medicos_profesionales4","tema_pacientes","tema_pacientes2"],
    "listas": ["solo_medicos1","solo_medicos2","solo_medicos3","solo_medicos4"
               ,"medicos_profesionales1",
              "medicos_profesionales2","medicos_profesionales3","medicos_profesionales4","pacientes","pacientes2"]
    }
def buscar_contenido_por_texto(obj):
    del obj["fecha"]
    
    retornos= []
    if "todos" in obj:
        retornos = obtener_recomendaciones_item(obj["todos"], crud.read_contenidos_procesados())
    else:

        lista = crud.read_contenidos_por_atributos(tipos[list(obj.keys())[0]])
        lista_consolidados = []
        for o in lista:
            consolidado = ""
            for v in o:
                consolidado = consolidado + " "+o[v]
            lista_consolidados.append({"id_contenido":o["id_contenido"],"contenido_procesado":consolidado})
        retornos = obtener_recomendaciones_item(list(obj.values())[0], lista_consolidados)
        # for o in tmp:
        #     consolidado_total = tmp["documento_procesado"]
            
        #     for p in obj:
        #         if p in tipos and p != "todos":
        #             consolidado_total = ""
        #             for c in tipos[p]:
        #                     if c in o:
        #                         consolidado_total = consolidado_total + o[c]+" "

        #     #if p != "fecha":
        #     #    if p in tipos:
        #     #        for c in tipos[p]:
        #     #            if c in o:
        #     #    else:
        #     #                consolidado_total = consolidado_total + o[c]+" "
        #     #        if p in o:
        #     #            consolidado_total = o[p]
                
        #         #consolidado = o["titulo"]+" "+o["resumen"]+" "+o["productos1"]+" "+o["productos2"]+" "+o["productos3"]+" "+o["productos4"]+" "+o["keyword1"]+" "+o["keyword2"]+" "+o["keyword3"]+" "+o["keyword4"]+" "+o["busqueda1"]+" "+o["busqueda2"]+" "+o["busqueda3"]
        #     #    for q in obj[p].split(" "):
        #     #        if q.lower() in consolidado_total.lower() and int(o["id_contenido"]) not in retornos:
            #            retornos.append(int(o["id_contenido"]))
    return retornos
def crear_contenido(salida):
    id = crud.read_contenido_by_item(salida["id_contenido"])
    ret = ""
    if id is None:
        ret = crud.create_contenido(salida)
        procesamiento_batch(ret)
    else:
        
        ret = crud.update_contenido(salida["id_contenido"],salida)
        procesamiento_batch(salida["id_contenido"])
    return ret
def crear_consumo(objeto):
    return crud.create_consumo(objeto )
def recomendar_contenido_home(obj):
    #LOGICA PENDIENTE CON SISTEMA DE RECOMENDACIÓN
    
    salida = crud.read_contenidos()
    retornos = {"tendencia":[],"recomendacion":[],"volveraver":[]}
    """for o in salida:
        retornos["tendencia"].append(int(o["id_contenido"]))
        retornos["recomendacion"].append(int(o["id_contenido"]))
        retornos["volveraver"].append(int(o["id_contenido"]))
    """
    retornos["tendencia"] = [201, 216, 220, 227, 234, 247, 265, 276, 278, 432]
    retornos["recomendacion"] = [201, 216, 220, 227, 234, 247, 265, 276, 278, 432]
    retornos["volveraver"] = [201, 216, 220, 227, 234, 247, 265, 276, 278, 432]
    
    return retornos
def recomendar_contenido_video(obj):
    #LOGICA PENDIENTE CON SISTEMA DE RECOMENDACIÓN
    
    retornos = {"tendencia":[],"recomendacion":[],"volveraver":[]}
    """for o in salida:
        retornos["tendencia"].append(int(o["id_contenido"]))
        retornos["recomendacion"].append(int(o["id_contenido"]))
        retornos["volveraver"].append(int(o["id_contenido"]))
    """
    retornos["tendencia"] = [201, 216, 220, 227, 234, 247, 265, 276, 278, 432]
    retornos["recomendacion"] = [201, 216, 220, 227, 234, 247, 265, 276, 278, 432]
    retornos["volveraver"] = [201, 216, 220, 227, 234, 247, 265, 276, 278, 432]
    
    return retornos
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
    

def remove_stop_words(dirty_text):
    cleaned_text = ''
    for word in dirty_text.split():
        if word in language_stopwords or word in non_words:
            continue
        else:
            cleaned_text += word + ' '
    return cleaned_text
def remove_punctuation(dirty_string):
    dirty_string = dirty_string.replace('á', 'a')
    dirty_string = dirty_string.replace('é', 'e')
    dirty_string = dirty_string.replace('í', 'i')
    dirty_string = dirty_string.replace('ó', 'o')
    dirty_string = dirty_string.replace('ú', 'u')
    return dirty_string
def procesar_documento(file_content):
    # All to lower case
    file_content = file_content.lower()
    # Remove punctuation and spanish stopwords
    file_content = remove_punctuation(file_content)
    file_content = remove_stop_words(file_content)
    return file_content
def procesamiento_batch(id=None):

    if id:
        lista = crud.read_contenido_by_item(id)
    else:
        lista = crud.read_contenidos()
    for o in lista:
        salida = ""
        for i in o:
            if i in tipos["todos"]:
                salida = salida + " "+o[i]
        procesar_documento(salida)
        crud.update_contenido(o["id_contenido"],{"documento_procesado":salida})

def obtener_recomendaciones_item(texto,lista):
    ds =  pd.DataFrame(list(lista))

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0)
    
    
    ds2 = pd.DataFrame([{"id_contenido":"","id_user": -1 ,"contenido":procesar_documento(texto)}])
    #ds = ds2.apply(lambda x: process_file(x) if x.name == 'contenido' else x)

    ds=ds.append(ds2, ignore_index = True)
    ds=ds.iloc[:, [1,0,2]]
    tfidf_matrix = tf.fit_transform(ds['contenido'])
    results = []
    similarity_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)
    for idx, row in ds.iterrows():
        if row["id_user"] == -1:
            similar_indices = similarity_matrix[idx].argsort()[:-100:-1]
            similar_items = [(similarity_matrix[idx][i], ds['id_user'][i]) for i in similar_indices]
            results= similar_items[1:]
        
    usrs_ret =[] 
    for o in results:
        if o[1] not in usrs_ret:
            usrs_ret.append(o[1])

    print(usrs_ret)
    return usrs_ret