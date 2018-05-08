from datetime import date, datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.urls import reverse_lazy
from django.core import validators
import re

from localflavor.br.br_states import STATE_CHOICES
from localflavor.br.models import BRStateField
import jwt
from django.conf import settings
from core.models import TimestampedModel

class User( AbstractBaseUser, PermissionsMixin, TimestampedModel ):

    # Informações Pessoais
    username = models.CharField(
        'Nome', max_length=50, unique=True, validators=[
            validators.RegexValidator(
                re.compile(
                    '/(?=^.{2,60}$)^[A-ZÀÁÂĖÈÉÊÌÍÒÓÔÕÙÚÛÇ][a-zàáâãèéêìíóôõùúç]+(?:[ ](?:das?|dos?|de|e|[A-Z][a-z]+))*$/'),
                'Informe um nome de usuário válido',
                'este valor deve conter apenas letras e espaços',
                'invalid'
            )
        ], help_text='Seu nome será usado para identifica-lo de forma única na plataforma')

    email = models.EmailField('Email', unique=True)


    # Informações Adicionais
    is_staff=models.BooleanField('Equipe', default=False)
    is_active=models.BooleanField('Ativo', default=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

    def get_absolute_url(self):
        return reverse_lazy('contas:usuario-info', kwargs={'pk': self.pk})
