from django.shortcuts import render
from django.views.generic import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User

from .forms import PasswordResetRequestForm, SetPasswordForm, UserRegister

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from django.conf import settings
from django.db.models.query_utils import Q
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
from django.contrib import messages

from django.contrib.auth import authenticate, login, forms, get_user_model
from django.core.exceptions import NON_FIELD_ERRORS

class RegistroDeUsuarioView(CreateView):

    model = User
    template_name = 'contas/login/registro.html'
    form_class = UserRegister
    success_url = '/'

    def form_valid(self, form):
        valid = super(RegistroDeUsuarioView, self).form_valid(form)
        username, password = form.cleaned_data.get(
            'username'), form.cleaned_data.get('password1')
       
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return valid

    def form_invalid(self, form):
        invalid = super(RegistroDeUsuarioView, self).form_invalid(form)

        return invalid
        

class ResetPasswordRequestView(FormView):
        # code for template is given below the view's code
        template_name = "contas/registration/reset_password.html"
        success_url = '/'
        form_class = PasswordResetRequestForm

        @staticmethod
        def validate_email_address(email):
            """
            Esse método aqui valida se o input é um email ou não. Retorna um booleano True se o input for um email e False se não for
            """
            try:
                validate_email(email)
                return True
            except ValidationError:
                return False

        def post(self, request, *args, **kwargs):
            """
            Um request post normal que pega o campo de input  "email"( no ResetPasswordRequestForm)
            """
            form = self.form_class(request.POST)
            if form.is_valid():
                data = form.cleaned_data["email"]
            # uses the method written above
            if self.validate_email_address(data) is True:
                """
                Se o input for um endereço válido de email o codigo seguinte vai buscar por usuários associados a esse email. Se encontrar um email será enviado para ele, se não uma mensagem de erro vai ser escrita na tela
                """
                associated_users = User.objects.filter(email=data)
                if associated_users.exists():
                    for user in associated_users:
                            c = {
                                'email': user.email,
                                'domain': request.META['HTTP_HOST'],
                                'site_name': 'BikeUnit',
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                                'user': user,
                                'token': default_token_generator.make_token(user),
                                'protocol': 'http',
                            }
                            subject_template_name = 'contas/registration/password_reset_subject.txt'
                            # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                            email_template_name = 'contas/registration/password_reset_email.html'
                            # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                            subject = loader.render_to_string(
                                subject_template_name, c)
                            # Email subject *must not* contain newlines
                            subject = ''.join(subject.splitlines())

                            email = loader.render_to_string(
                                email_template_name, c)

                            send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [
                                      user.email], fail_silently=False)
                    result = self.form_valid(form)
                    messages.success(request, 'Um email foi enviado para ' + data +
                                     ". Por favor, olhe sua caixa de entrada para recuperar a sua senha.")
                    return result
                result = self.form_invalid(form)
                messages.error(
                    request, 'Nenhum usuário associado a este endereço de email')
                return result

            messages.error(request, 'Entrada Inválida')
            return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    template_name = "contas/registration/reset_password.html"
    success_url = '/'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        Checa o token do  link de recuperação  e apresenta o formuláro para inserir o novo password        
        """
        user_model = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = user_model._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user_model.DoesNotExist) as e:
            print(e)
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'A senha foi alterada com sucesso.')
                return self.form_valid(form)
            else:
                messages.error(
                    request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(
                request, 'Este link não é mais válido.')
            return self.form_invalid(form)
