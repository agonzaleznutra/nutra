from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/filter', views.busqueda_contenido, name='filter'),
    url(r'^/get_recom', views.recomendacion_home, name='get_recom'),
    url(r'^/recom_video', views.recomendacion_video, name='get_recom_video'),
    url(r'^/load_content', views.view_crear_contenido, name='load_content'),
    url(r'^/set_consumo', views.view_crear_consumo, name='set_consumo'),
    url(r'^/load_user', views.view_crear_usuario, name='load_user'),
    

]