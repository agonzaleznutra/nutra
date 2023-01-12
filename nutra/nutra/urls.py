from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from recomendador import views
urlpatterns = [
    path(r'^apis', include('recomendador.urls')),
    path(r'^admin', admin.site.urls),
    path(r'^app', views.index, name='index'),
    path(r'^health', views.health, name='health'),
    
]