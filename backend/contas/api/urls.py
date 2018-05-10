
from django.urls import path, re_path

from contas.api.views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView

app_name='api_auth'

urlpatterns = [
    path('usuario/atualiza/', UserRetrieveUpdateAPIView.as_view()),
    path('usuario/registra/', RegistrationAPIView.as_view()),
    path('usuario/login/', LoginAPIView.as_view())
]
