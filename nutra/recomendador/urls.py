from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_recom', views.recomendacion, name='get_recom'),
    url(r'^health', views.health),

]