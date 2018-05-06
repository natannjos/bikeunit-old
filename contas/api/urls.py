
from django.urls import path, re_path

from contas.api.views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView

app_name='api_auth'

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view())

]
