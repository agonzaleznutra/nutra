from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from recomendador import views
urlpatterns = [
    path('apis', include('recomendador.urls')),
    path('admin', admin.site.urls),
    path('app', views.index, name='index'),
    path('health', views.health, name='health'),
    
]