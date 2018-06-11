from .views import home, contato
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('contato', contato, name='contato'),
]