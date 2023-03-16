from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/filter', views.filter, name='filter'),
    url(r'^/get_recom', views.recomendacion, name='get_recom'),
    url(r'^/load_content', views.load_content, name='load_content'),
    url(r'^/set_consumo', views.set_consumo, name='set_consumo'),

]