from .views import UserInfo
from django.urls import path

app_name = 'contas'

urlpatterns = [
    path('info/<int:pk>', UserInfo.as_view(), name='user-info')
]
