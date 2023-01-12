from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

urlpatterns = [
    path('app/', include('recomendador.urls')),
    path('admin/', admin.site.urls),
    #path('get_recom', views.recomendacion, name='get_recom'),
    #url(r'^health', views.health),
]