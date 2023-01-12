from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    
    url(r'^/get_recom', views.recomendacion, name='get_recom'),

]