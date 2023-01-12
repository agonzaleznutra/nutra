from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('health', views.health, name='health'),
    path('get_recom', views.recomendacion, name='get_recom'),

]