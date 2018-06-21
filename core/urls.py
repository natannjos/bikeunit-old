from .views import home, contato, busca_grupo_por_localidade
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('contato', contato, name='contato'),
    path('ajax/atualiza', busca_grupo_por_localidade, name="atualiza")
]
