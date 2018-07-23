from django.urls import path
from grupos import views

app_name='grupos'

urlpatterns = [
    path('grupos-admin', views.grupos_admin_lista, name='grupos-admin'),
    path('<slug:slug>', views.grupo_info, name='grupo_info'),
]
