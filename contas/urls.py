from .views import ResetPasswordRequestView, PasswordResetConfirmView, RegistroDeUsuarioView
from django.urls import path

app_name = 'contas'

urlpatterns = [
    path('reset-senha', ResetPasswordRequestView.as_view(), name="reset-senha"),
    path('confirma-reset-senha/reset_password_confirm/<slug:uidb64>/<slug:token>',
         PasswordResetConfirmView.as_view(), name='confirma-reset-senha'),
    path('registro', RegistroDeUsuarioView.as_view(), name='registra-conta' )
]
