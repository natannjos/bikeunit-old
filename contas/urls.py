from .views import ResetPasswordRequestView, PasswordResetConfirmView
from django.urls import path

app_name = 'contas'

urlpatterns = [
    path('reset-senha', ResetPasswordRequestView.as_view(), name="reset-senha"),
    path('confirma-reset-senha/reset_password_confirm/<slug:uidb64>/<slug:token>',
         PasswordResetConfirmView.as_view(), name='confirma-reset-senha'),
]
