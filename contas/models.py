from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.urls import reverse_lazy
from django.core import validators
import re

from localflavor.br.br_states import STATE_CHOICES
from localflavor.br.models import BRStateField


class User( AbstractBaseUser, PermissionsMixin ):

    # Informações Pessoais
    username = models.CharField(
        'Nome ou email', max_length=50, unique=True, validators=[
            validators.RegexValidator(
                re.compile(
                    '/(?=^.{2,60}$)^[A-ZÀÁÂĖÈÉÊÌÍÒÓÔÕÙÚÛÇ][a-zàáâãèéêìíóôõùúç]+(?:[ ](?:das?|dos?|de|e|[A-Z][a-z]+))*$/'),
                'Informe um nome de usuário válido',
                'este valor deve conter apenas letras e espaços',
                'invalid'
            )
        ], help_text='Seu nome será usado para identifica-lo de forma única na plataforma'
    )

    amigos = models.ManyToManyField('self', related_name='Amigos', verbose_name='Meus Amigos', blank=True)
    convites_recebidos = models.ManyToManyField('self', related_name='convites_recebidos', verbose_name='Convites Recebidos', blank=True)
    convites_enviados = models.ManyToManyField(
        'self', related_name='convites_enviados', verbose_name='Convites Enviados', blank=True)
    meus_grupos = models.ManyToManyField('grupos.Grupos', related_name='meus_grupos', verbose_name='Meus Grupos', blank=True)
    pedais_gratis = models.ManyToManyField('grupos.Pedal', related_name='pedais_gratis', verbose_name='Pedais Gratis', blank=True)
    
    pedais_agendados = models.ManyToManyField('grupos.Pedal', related_name='pedais_agendados', verbose_name='Pedais Marcados', blank=True)

    email = models.EmailField('Email', unique=True)

    sexos = (
        ('1', 'Masculino'),
        ('2', 'Feminino'),
        )
    sexo = models.CharField('Sexo', max_length=1, choices=sexos, blank=True, null=True)

    nascimento = models.DateField('Data de Nascimento', blank=True, null=True)
    phone_digits_re=re.compile(r'^[(\.](\d{2})[)\.]?(\d{4,5})[-\.]?(\d{4})$')
    telefone = models.CharField('Telefone', max_length=15, validators=[validators.RegexValidator(phone_digits_re)])
    tel_emergencia = models.CharField('Telefone de emergências', max_length=15, validators=[validators.RegexValidator(phone_digits_re)])

    # Documentos
    cpf_digits_re=re.compile(r'^(\d{3})\.(\d{3})\.(\d{3})-(\d{2})$')
    cpf=models.CharField(
        'CPF', max_length = 14,
        validators = [validators.RegexValidator(cpf_digits_re)],
        blank = True, null = True, unique = True
    )

    # Endereço    
    cep_digits_re = re.compile(r'^(\d{5})-(\d{3})$')
    cep = models.CharField('CEP', max_length=10, validators=[validators.RegexValidator(cep_digits_re)])
    rua = models.CharField('Endereço', max_length=50)
    bairro = models.CharField('Bairro', max_length=50)
    cidade = models.CharField('Cidade', max_length=50)
    estado = BRStateField('Estado', choices=STATE_CHOICES, max_length=2)

    # Informações Adicionais
    is_staff=models.BooleanField('Equipe', default=False)
    is_admin = models.BooleanField('Admin', default=False)
    is_active=models.BooleanField('Ativo', default=True)
    date_joined=models.DateTimeField('Data de Entrada', auto_now_add=True)

    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return str(self)

    def get_short_name(self):
        return str(self).split(" ")[0]

    def nice_birth_date(self):
        nice_time = self.nascimento.strftime("%d/%m/%Y")
        return nice_time

    @property
    def historico_de_pedais(self):
        return self.pedais_agendados.filter(data__lt=date.today())
        #return list(filter(lambda x: x.data < date.today(), self.pedais_agendados.all()))

    @property
    def idade(self):
        today=date.today()
        if self.nascimento:
            try:
                birthday = self.nascimento.replace(year=today.year)
            except ValueError:
                # raised when birth date is February 29 and the current year is not a leap year
                birthday = self.nascimento.replace(
                                    year=today.year, month=self.nascimento.month + 1, day=1)
            finally:
                if birthday > today:
                    return today.year - self.nascimento.year - 1
                else:
                    return today.year - self.nascimento.year
        return '-'

    def save(self, *args, **kwargs):
        if self.nascimento == date.today():
            self.nascimento = None
        super(User, self).save(*args, **kwargs) # Call the real save() method

    def get_absolute_url(self):
        return reverse_lazy('contas:usuario-info', kwargs={'pk': self.pk})