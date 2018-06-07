from .views import home
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('', home, name='home')
]