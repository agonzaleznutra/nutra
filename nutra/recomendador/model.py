from pymongo import MongoClient
import urllib.parse

username = urllib.parse.quote_plus('aleja_user')
password = urllib.parse.quote_plus('02-10-91aldigovE')
url_bd = "172.31.22.3"
class crud():
    mc =MongoClient(str("mongodb://%s:%s@%s") % (username, password,url_bd))
    def read_contenidos():
        return mc.nutra.contenidos.find({},{"documento_procesado":0,"_id":0})
    def read_contenidos_procesados():
        return mc.nutra.contenidos.find({},{"documento_procesado":1,"id_contenido":1,"_id":0})
    def read_contenidos_por_atributos(atributos):
        filtro = {"id_contenido":1,"_id":0}
        for o in atributos:
            filtro[o]=1
        return mc.nutra.contenidos.find({},filtro)
    def read_contenido_by_item(id):
        return mc.nutra.contenidos.find_one({"id_contenido":id})
    def create_contenido(object):
        mc.nutra.contenidos.insert_one(object)
        return object["id_contenido"]
    def update_contenido(id,object):
        mc.nutra.contenidos.update_one({"id_contenido":id},{"$set":object})
        return "ok"
    def create_consumo(object):
        mc.nutra.consumos.insert_one(object)
        return "ok"
