from pymongo import MongoClient
import urllib.parse

username = urllib.parse.quote_plus('aleja_user')
password = urllib.parse.quote_plus('02-10-91aldigovE')
url_bd = "172.31.22.3"
class crud():
    def __init__(self):
        self.mc =MongoClient(str("mongodb://%s:%s@%s") % (username, password,url_bd))
    
    def read_contenidos(self):
        return self.mc.nutra.contenidos.find({},{"documento_procesado":0,"_id":0})
    def read_contenidos_procesados(self):
        return self.mc.nutra.contenidos.find({},{"documento_procesado":1,"id_contenido":1,"_id":0})
    def read_contenidos_por_atributos(self,atributos):
        filtro = {"id_contenido":1,"_id":0}
        for o in atributos:
            filtro[o]=1
        return self.mc.nutra.contenidos.find({},filtro)
    def read_contenido_by_item(self,id):
        return self.mc.nutra.contenidos.find({"id_contenido":id},{"_id":0})
    def create_contenido(self,object):
        self.mc.nutra.contenidos.insert_one(object)
        return object["id_contenido"]
    def update_contenido(self,id,object):
        self.mc.nutra.contenidos.update_one({"id_contenido":id},{"$set":object})
        return "ok"
    def create_consumo(self,object):
        self.mc.nutra.consumos.insert_one(object)
        return "ok"
