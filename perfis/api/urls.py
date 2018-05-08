from django.urls import path

from perfis.api.views import ProfileRetrieveAPIView

app_name = "profiles"

urlpatterns = [
    path('perfil/<int:pk>/', ProfileRetrieveAPIView.as_view()),
]
