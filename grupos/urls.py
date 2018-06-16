from django.urls import path
from .views import grupos_admin_lista

app_name='grupos'

urlpatterns = [
    path('grupos-admin', grupos_admin_lista, name='grupos-admin')
]
