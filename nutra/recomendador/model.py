from pymongo import MongoClient
import urllib.parse

username = urllib.parse.quote_plus('aleja_user')
password = urllib.parse.quote_plus('02-10-91aldigovE')
url_bd = "172.31.22.3"
#url_bd = "44.209.53.70"
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
    def read_usuario_by_id(self,id):
        return self.mc.nutra.usuarios.find({"id":id},{"_id":0})
    def read_usuario_mas_consumos(self):
        pipeline = [{'$group': {'_id': '$id_usuario','count': {'$sum': 1}}},{'$sort': {'count': -1}}]
        return self.mc.nutra.consumos.aggregate(pipeline)
    def read_consumos_by_user(self,id_user):
        return self.mc.nutra.consumos.find({"id_usuario":id_user},{"_id":0,"id_contenido":1,"fecha":1})
    def read_consumos_by_agrupacion_contenido(self):
        pipeline = [{'$group': {'_id': '$id_contenido','count': {'$sum': 1}}},{'$sort': {'count': -1}}]
        return self.mc.nutra.consumos.aggregate(pipeline)

    def create_contenido(self,object):
        self.mc.nutra.contenidos.insert_one(object)
        return object["id_contenido"]
    def update_contenido(self,id,object):
        self.mc.nutra.contenidos.update_one({"id_contenido":id},{"$set":object})
        return "ok"
    def update_usuario(self,id,object):
        self.mc.nutra.usuarios.update_one({"id":id},{"$set":object})
        return "ok"
    def create_consumo(self,object):
        self.mc.nutra.consumos.insert_one(object)
        return "ok"
