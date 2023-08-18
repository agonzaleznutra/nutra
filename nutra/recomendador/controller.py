from string import punctuation
non_words = list(punctuation)
from nltk.corpus import stopwords
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import nltk
nltk.download('wordnet')
from .model import crud
import datetime
import json
import time
import inspect

language_stopwords = stopwords.words('spanish')
#los tipos de consulta define consultas que validan contra varios campos un valor y son predefinidas
map = {"desplegable3":"sujetoconocimientomf"}
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
    "data_visible2":["resumen"] ,
    "data_invisible" : ["presentador",
              "productos1","productos2","productos3","productos4",
              "productos5","productos6","productos7","productos8",
              "productos9","productos10","productos11","productos12","productos13","productos14","productos15","productos16","productos17",
              "keyword1","keyword2","keyword3","keyword4","keyword5","keyword6",
              "keyword_diagnostico","contenido_orientacion4",
              "busqueda1","busqueda2","busqueda3",
              "cincor",
              "solo_medicos1","solo_medicos2","solo_medicos3","solo_medicos4","medicos_profesionales1",
              "medicos_profesionales2","medicos_profesionales3","medicos_profesionales4","pacientes","pacientes2"]
    }


class tiempo:
    def __init__(self):
        self.t1 = {"h":time.time(),"i":0}
        pass
    def prnt_time(self,l):
        t2 = time.time()
        print("t"+str(self.t1["i"])+":l"+str(l)+":", t2-self.t1["h"], "segundos")
        self.t1["h"] = t2
        self.t1["i"] = self.t1["i"]+1
        
class views_control:
    def crear_contenido(self,salida):
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
    def crear_relations(self,objeto):
        return crud().create_relacion(objeto )
    def crear_usuario(self,salida):
        print("salida.....",salida)
        salida["id"] = salida["idUser"]
        results = list(crud().read_usuario_by_id(salida["id"]))
        ret = ""
        if len(results)==0:
            ret = crud().create_usuario(salida)
            print("user_ creado...",ret)
        else:
            
            ret = crud().update_usuario(salida["id"],salida)
            print("user actualizado...",ret)
        return ret
    def crear_consumo(self,objeto):
        return crud().create_consumo(objeto )
    def recomendar_contenido_video(self,obj):
        #LOGICA PENDIENTE CON SISTEMA DE RECOMENDACIÓN
        print("entrada...video...",obj)
        
        salida = {"recomendacion":logic().get_usuario_por_video(obj["id_user"],[{"id_contenido":obj["id_contenido"]}])}
        print("sal...video..",salida)
        return salida   
    def buscar_contenido_por_texto(self,obj):
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
    
    def recomendar_contenido_home(self,obj):
        import time
        t1 = tiempo()
        #INICIALIZA RETORNO
        retornos = {"tendencia":[],"recomendacion":[],"volveraver":[]}
        
        t1.prnt_time(inspect.currentframe().f_lineno)
        #CONSULTA LOS CONTENIDOS TENDENCIA Y LOS ASIGNA AL RETORNO
        lista = crud().read_consumos_by_agrupacion_contenido()
        t1.prnt_time(inspect.currentframe().f_lineno)
        valida_user = list(crud().read_usuario_by_id(obj["id_user"]))
        t1.prnt_time(inspect.currentframe().f_lineno)
        for o in list(lista)[0:20]:
            retornos["tendencia"].append(int(o["_id"]))
        #PREGUNTA SI NO TRAE ID DE USUARIO
        t1.prnt_time(inspect.currentframe().f_lineno)
        retornos["todos"] = []
        lista_todos = list(crud().read_contenidos_by_query({"busqueda2":"Todos"},["id_contenido"]))
        t1.prnt_time(inspect.currentframe().f_lineno)
        for i in lista_todos:
            retornos["todos"].append(int(i["id_contenido"]))
            
        t1.prnt_time(inspect.currentframe().f_lineno)
        if "id_user" not in obj or len(valida_user) == 0:
            #TRAE ID DE USUARIO? NO
            #TRAE LISTA DE CONTENIDOS INICIALES EN LA ESCALERA
            t1.prnt_time(inspect.currentframe().f_lineno)
            lista_basicos = list(crud().read_contenidos_by_query({"sujetoconocimientomf":"NO SABE NADA","sujetoamornb":"ODIA"},["id_contenido"]))
            #MEZCLA 50-50 LAS TENDENCIAS CON OS CONTENIDOS INICIALES EN LA ESCALERA
            t1.prnt_time(inspect.currentframe().f_lineno)
            for i in range(10):
                retornos["recomendacion"].append(int(lista_basicos[i]["id_contenido"]))
                retornos["recomendacion"].append(retornos["tendencia"][i])
            t1.prnt_time(inspect.currentframe().f_lineno)
        else:
            #TRAE ID DE USUARIO? SI
            t1.prnt_time(inspect.currentframe().f_lineno)
            lista_bu = list(crud().read_consumos_by_user(obj["id_user"]))
            #EL USUARIO YA HA VISTO CONTENIDOS? NO        
            t1.prnt_time(inspect.currentframe().f_lineno)    
            if len(lista_bu) == 0:
                retornos["volveraver"]= []
                retornos["recomendacion"] = logic().get_usuario_ha_visto_videos_n2(obj["id_user"],[70,30])
                t1.prnt_time(inspect.currentframe().f_lineno)
            #EL USUARIO YA HA VISTO CONTENIDOS? SI
            else:
                t1.prnt_time(inspect.currentframe().f_lineno)
                retornos["recomendacion"] = logic().get_usuario_ha_visto_videos(obj["id_user"],lista_bu)
                t1.prnt_time(inspect.currentframe().f_lineno)
                for o in lista_bu:
                    retornos["volveraver"].append(int(o["id_contenido"]))
                t1.prnt_time(inspect.currentframe().f_lineno)
        retornos["solo_aqui"] = [201, 216, 220, 227, 234, 247, 265, 276, 278, 432]
        print("resultados...",retornos)
        t1.prnt_time(inspect.currentframe().f_lineno)
        return retornos

class logic:
    def distribuir_proporciones(self,arrs,proporcion):
        retornos = []
        tam_salida = 20
        tams = [0,0,0]
        for i,o in enumerate(proporcion):
            tams[i] = round(tam_salida * (o/100))
        for i,o in enumerate(tams):
            for j in range(o):
                if j == len(arrs[i]):
                    break
                retornos.append(arrs[i][j])
        return retornos
    def get_usuario_ha_visto_videos_n2(self,id_user,proporcion):
        t1 = tiempo()
        lista_por_categoria = []
        #3. BUSCA CONTENIDOS CON LA CATEGORIA DE MI USUARIO
        categorias_usuario = ["desplegable3"]
        query_categorias = {}
        t1.prnt_time(inspect.currentframe().f_lineno)
        print(id_user)
        tmp_categoria_usuario = list(crud().read_usuario_by_id(id_user))[0]
        t1.prnt_time(inspect.currentframe().f_lineno)
        for o in categorias_usuario:
            try:
                query_categorias[map[o]]=tmp_categoria_usuario[o]
            except:
                print(o,"no esta")
        t1.prnt_time(inspect.currentframe().f_lineno)
        
        tmp_lista_por_categoria = list(crud().read_contenidos_by_query(query_categorias,["id_contenido"]))
        t1.prnt_time(inspect.currentframe().f_lineno)
        for o in tmp_lista_por_categoria:
            lista_por_categoria.append(int(o["id_contenido"]))
        #4. BUSCA CONTENIDO SIMILAR AL ANTERIOR
        t1.prnt_time(inspect.currentframe().f_lineno)
        print("control....",len(tmp_lista_por_categoria))
        lista_cola_larga = logic().buscar_similares_a_contenidos(tmp_lista_por_categoria)
        t1.prnt_time(inspect.currentframe().f_lineno)
        return logic().distribuir_proporciones([lista_por_categoria,lista_cola_larga],proporcion)
    def get_usuario_ha_visto_videos(self,id_user,contenidos):
        t1 = tiempo()
        #5. BUSCA CONTENIDOS SIMILARES A LOS VISTOS O AL ACTUAL
        
        lista_similar = logic().buscar_similares_a_contenidos(contenidos)
        t1.prnt_time(inspect.currentframe().f_lineno)
        lista_n2 = logic().get_usuario_ha_visto_videos_n2(id_user,[66,33])
        t1.prnt_time(inspect.currentframe().f_lineno)
        lista_n3 = logic().distribuir_proporciones([lista_similar,lista_n2],[40,60])
        t1.prnt_time(inspect.currentframe().f_lineno)
        return lista_n3
        
        
    def get_usuario_por_video(self,id_user,contenidos):
        
        #5. BUSCA CONTENIDOS SIMILARES A LOS VISTOS O AL ACTUAL
        lista_similar = logic().buscar_similares_a_contenidos(contenidos)
        lista_n2 = logic().get_usuario_ha_visto_videos_n2(id_user,[50,50])
        lista_n3 = logic().distribuir_proporciones([lista_similar,lista_n2],[60,40])
        return lista_n3
    def extraccion_atributos_en_objeto(self,obj):
        
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
    def buscar_similares_a_contenidos(self,conts):
        
        t1 = tiempo()
        salida = []
        lista = list(crud().read_contenidos_procesados())
        t1.prnt_time(inspect.currentframe().f_lineno)
        for o in conts[0:3]:
            ds0 = list(crud().read_relaciones_by_id_contenido_origen(o))
            for i in ds0:
                if i not in salida:
                    salida.append(int(i["id_contenido_destino"]))
            if len(salida) < 20:
                ds1 = obtener_recomendaciones_id(o["id_contenido"], lista,0.1)        
                for i in ds1:
                    if i not in salida:
                        salida.append(i)
                        if len(salida) > 20:
                            break
            t1.prnt_time(inspect.currentframe().f_lineno)
        t1.prnt_time(inspect.currentframe().f_lineno)
        return salida   

def remove_stop_words(dirty_text):
    cleaned_text = ''
    for word in dirty_text.split():
        if word in language_stopwords:
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
    for o in non_words:
        dirty_string = dirty_string.replace(o, '')
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
        for k,v in o.items():
            if k != "id_contenido":
                consolidado = consolidado + " "+v
        lista_consolidados.append({"id_contenido":o["id_contenido"],"documento_procesado":consolidado})
    
    ds1 = obtener_recomendaciones_item(texto, lista_consolidados)
    print("primera busqueda........",ds1)



    lista = crud().read_contenidos_por_atributos(tipos["data_visible2"])
    lista_consolidados = []
    for o in lista:
        consolidado = ""
        if int(o["id_contenido"]) not in ds1:
            for k,v in o.items():
                if k != "id_contenido":
                    consolidado = consolidado + " "+v
            lista_consolidados.append({"id_contenido":o["id_contenido"],"documento_procesado":consolidado})
    ds2 = obtener_recomendaciones_item(texto, lista_consolidados)
    for o in ds2:
        if o not in ds1:
            ds1.append(o)
    print("segunda busqueda........",ds1)


    lista = crud().read_contenidos_por_atributos(tipos["data_invisible"])
    lista_consolidados = []
    for o in lista:
        consolidado = ""
        if int(o["id_contenido"]) not in ds1:
            for k,v in o.items():
                if k != "id_contenido":
                    consolidado = consolidado + " "+v
            lista_consolidados.append({"id_contenido":o["id_contenido"],"documento_procesado":consolidado})
    
    ds3 = obtener_recomendaciones_item(texto, lista_consolidados,0.001)
    
    
    print("resultado final....",{"resultados":ds1,"recomendaciones":ds3})
    return {"resultados":ds1,"recomendaciones":ds3}

def custom_tokenizer(text):
    lemmatized_tokens = []
    tokens = procesar_documento(text).split()  # Dividir el texto en palabras
    for token in tokens:
        lt = lemmatizer.lemmatize(token)
        if lt not in tokens:
            lemmatized_tokens.append(lt)
    
    #lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]  # Lematizar cada palabra
    combined_tokens = tokens + lemmatized_tokens  # Combinar palabras normales y lematizadas
    return combined_tokens
def obtener_recomendaciones_id(id,lista,th = 0.05):
    
    ds =  pd.DataFrame(list(lista))
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0)
    usrs_ret =[] 
    tfidf_matrix = tf.fit_transform(ds['documento_procesado'])
    results = []
    similarity_matrix = cosine_similarity(tfidf_matrix)
    for idx, row in ds.iterrows():
        if row["id_contenido"] == id:
            #similar_indices = similarity_matrix[idx].argsort()[:-100:-1]
            similar_indices = [i for i, x in enumerate(similarity_matrix[idx]) if x > th]
            similar_items = [(similarity_matrix[idx][i], ds['id_contenido'][i]) for i in similar_indices]
            similar_items.sort(reverse = True)
            results= similar_items[1:]
        
    for o in results:
        if int(o[1]) not in usrs_ret:
            usrs_ret.append(int(o[1]))

    return usrs_ret
def obtener_recomendaciones_item(texto,lista,th = 0.05):
    salida = []
    texto_tokenizado = custom_tokenizer(texto)
    print(texto_tokenizado)
    for o in lista:
        grado = 0
        for u in texto_tokenizado:
            if u in " ".join(custom_tokenizer(o["documento_procesado"])):
                grado += 1
        if grado > 0:
            salida.append({"id":o["id_contenido"],"grado":grado/len(texto_tokenizado)})
    print(salida)
    salida = sorted(salida, key=lambda x: x['grado'],reverse=True)
    return [int(d['id']) for d in salida]


