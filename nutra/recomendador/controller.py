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
              "medicos_profesionales2","medicos_profesionales3","medicos_profesionales4","pacientes","pacientes2"],
    "data_visible":["titulo","tema_solo_medicos1","tema_solo_medicos2","tema_solo_medicos3","tema_solo_medicos4","tema_medicos_profesionales1",
              "tema_medicos_profesionales2","tema_medicos_profesionales3","tema_medicos_profesionales4","tema_pacientes","tema_pacientes2"],
    "data_visible2":["resumen"] 
    }
def buscar_contenido_por_texto(obj):
    del obj["fecha"]
    
    retornos= []
    if "todos" in obj:
        retornos = buscar_por_texto_completo(obj["todos"])
    else:

        lista = crud().read_contenidos_por_atributos(tipos[list(obj.keys())[0]])
        lista_consolidados = []
        for o in lista:
            consolidado = ""
            for v in o:
                consolidado = consolidado + " "+o[v]
            lista_consolidados.append({"id_contenido":o["id_contenido"],"documento_procesado":consolidado})
        retornos = obtener_recomendaciones_item(list(obj.values())[0], lista_consolidados)
    return retornos
def crear_contenido(salida):
    results = list(crud().read_contenido_by_item(salida["id_contenido"]))
    ret = ""
    if len(results)==0:
        ret = crud().create_contenido(salida)
        print("creado...",ret)
        procesamiento_batch(ret)
    else:
        
        ret = crud().update_contenido(salida["id_contenido"],salida)
        procesamiento_batch(salida["id_contenido"])
        print("actualizado...",ret)
    return ret
def crear_consumo(objeto):
    return crud().create_consumo(objeto )
def recomendar_contenido_home(obj):
    #LOGICA PENDIENTE CON SISTEMA DE RECOMENDACIÓN
    
    salida = crud().read_contenidos()
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
    print(id, type(id))
    if id:
        lista = crud().read_contenido_by_item(id)
    else:
        lista = crud().read_contenidos()
    for o in lista:
        salida = ""
        for i in o:
            if i in tipos["todos"]:
                salida = salida + " "+o[i]
        procesar_documento(salida)
        print(o)
        print(o["id_contenido"])
        crud().update_contenido(o["id_contenido"],{"documento_procesado":salida})
def buscar_por_texto_completo(texto):
    lista = crud().read_contenidos_por_atributos(tipos["data_visible"])
    lista_consolidados = []
    for o in lista:
        consolidado = ""
        for v in o:
            consolidado = consolidado + " "+o[v]
        lista_consolidados.append({"id_contenido":o["id_contenido"],"documento_procesado":consolidado})
    print("primera busqueda........")
    ds1 = obtener_recomendaciones_item(texto, lista_consolidados)
    lista = crud().read_contenidos_por_atributos(tipos["data_visible2"])
    lista_consolidados = []
    for o in lista:
        consolidado = ""
        for v in o:
            consolidado = consolidado + " "+o[v]
        lista_consolidados.append({"id_contenido":o["id_contenido"],"documento_procesado":consolidado})
    print("segunda busqueda........",ds1)
    ds2 = obtener_recomendaciones_item(texto, lista_consolidados)
    for o in ds2:
        if o not in ds1:
            ds1.append(o)
    lista = crud().read_contenidos_por_atributos(tipos["todos"])
    lista_consolidados = []
    for o in lista:
        consolidado = ""
        for v in o:
            consolidado = consolidado + " "+o[v]
        lista_consolidados.append({"id_contenido":o["id_contenido"],"documento_procesado":consolidado})
    print("tercera busqueda........",ds1)
    ds3 = obtener_recomendaciones_item(texto, lista_consolidados)
    ds4 = []
    for o in ds3:
        if o not in ds1:
            ds4.append(o)
    print("resultado final....",{"resultados":ds1,"recomendaciones":ds4})
    return {"resultados":ds1,"recomendaciones":ds4}
def obtener_recomendaciones_item(texto,lista):
    ds =  pd.DataFrame(list(lista))

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0)
    
    
    ds2 = pd.DataFrame([{"id_contenido":-1,"documento_procesado":procesar_documento(texto)}])

    ds=ds.append(ds2, ignore_index = True)
    ds=ds.iloc[:, [1,0]]

    tfidf_matrix = tf.fit_transform(ds['documento_procesado'])
    results = []
    similarity_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)
    for idx, row in ds.iterrows():
        if row["id_contenido"] == -1:
            similar_indices = similarity_matrix[idx].argsort()[:-100:-1]
            similar_items = [(similarity_matrix[idx][i], ds['id_contenido'][i]) for i in similar_indices]
            results= similar_items[1:]
        
    usrs_ret =[] 
    for o in results:
        if o[1] not in usrs_ret:
            usrs_ret.append(int(o[1]))

    print(usrs_ret)
    return usrs_ret