from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/cotacoes/', views.get_cotacoes_api, name='get_cotacoes_api'),
    path('api/cotacoes/db/', views.get_cotacoes_db_api, name='get_cotacoes_db_api'), # NOVO: API para ler do DB
]
