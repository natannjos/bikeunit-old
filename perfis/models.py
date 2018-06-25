from django.db import models
from core.models import TimestampedModel
from django.core import validators
import re

from localflavor.br.br_states import STATE_CHOICES
from localflavor.br.models import BRStateField

from datetime import date
from django.urls import reverse_lazy
from annoying.fields import AutoOneToOneField

class Profile(TimestampedModel):
    
    objects = models.Manager()

    user = AutoOneToOneField('contas.User', primary_key=True, on_delete=models.CASCADE)
    nome = models.CharField('Nome Completo', max_length=255)
    image = models.ImageField('Foto', blank=True, null=True, upload_to='perfis/foto')

    meus_grupos = models.ManyToManyField(
        'grupos.Grupos',
        related_name='meus_grupos',
        verbose_name='Meus Grupos',
        blank=True)

    grupos_deletados = models.ManyToManyField(
        'grupos.Grupos',
        related_name='grupos_deletados',
        verbose_name='Grupos Deletados',
        blank=True
    )

    pedais_agendados = models.ManyToManyField(
        'grupos.Pedal',
        related_name='pedais_agendados',
        verbose_name='Pedais Marcados',
        blank=True)

    pedais_deletados = models.ManyToManyField(
        'grupos.Pedal',
        related_name='pedais_deletados',
        verbose_name='Pedais Excluidos',
        blank=True)

    sexos = (
        ('1', 'Masculino'),
        ('2', 'Feminino'),
    )
    sexo = models.CharField(
        'Sexo',
        max_length=1,
        choices=sexos,
        blank=True,
        null=True)

    nascimento = models.DateField('Data de Nascimento', blank=True, null=True)
    phone_digits_re = re.compile(r'^[(\.](\d{2})[)\.]?(\d{4,5})[-\.]?(\d{4})$')
    telefone = models.CharField(
        'Telefone',
        max_length=15,
        validators=[validators.RegexValidator(phone_digits_re)],
        blank=True)
    tel_emergencia = models.CharField(
        'Telefone de emergências',
        max_length=15,
        validators=[validators.RegexValidator(phone_digits_re)],
        blank=True)

    is_admin = models.BooleanField('Admin', default=False)

    # Localização
    cidade = models.CharField('Cidade', max_length=50, blank=True)
    estado = BRStateField('Estado', choices=STATE_CHOICES, max_length=2, blank=True)

    def __str__(self):
        return self.user.username

    def get_short_name(self):
        return str(self).split(" ")[0]

    def nice_birth_date(self):
        nice_time = self.nascimento.strftime("%d/%m/%Y")
        return nice_time

    @property
    def historico_de_pedais(self):
        #return list(filter(lambda x: x.data < date.today(), self.pedais_agendados.all()))
        return self.pedais_agendados.filter(data__lt=date.today())

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


    #def get_absolute_url(self):
    #    return reverse_lazy('perfil:usuario-info', kwargs={'pk': self.pk})

