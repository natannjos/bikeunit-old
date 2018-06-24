from django.urls import path
from .views import grupos_admin_lista, grupo_info

app_name='grupos'

urlpatterns = [
    path('grupos-admin', grupos_admin_lista, name='grupos-admin'),
    path('<slug:slug>', grupo_info, name='grupo_info')
]
