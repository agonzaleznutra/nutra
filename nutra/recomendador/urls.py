from django.urls import path

from . import views

urlpatterns = [
    
    path('get_recom', views.recomendacion, name='get_recom'),

]