from django.urls import path
from perfis import views

app_name = 'perfis'
urlpatterns = [
    path('pedal/<int:pk>/sair', views.sair_de_pedal, name='sair-de-pedal')
]
