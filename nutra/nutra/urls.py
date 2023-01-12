from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from recomendador import views
urlpatterns = [
    url(r'^apis', include('recomendador.urls')),
    url(r'^admin', admin.site.urls),
    url(r'^index', views.index, name='index'),
    url(r'^health', views.health, name='health'),
    
]