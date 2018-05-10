from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.conf import settings
# Create your models here.
class Grupos(models.Model):
    objects = models.Manager()

    admin = models.ManyToManyField(settings.AUTH_USER_MODEL,
                              verbose_name='Administradores', related_name='admin')
    nome = models.CharField('Nome do grupo', max_length=20, unique=True)
    slug = models.SlugField()
    criacao = models.DateTimeField('Criado em', auto_now_add=True)
    modificacao = models.DateTimeField('Modificado em', auto_now=True)

    participantes = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Participantes', blank=True, related_name='Participantes')
    pedais = models.ManyToManyField('grupos.Pedal', verbose_name='Pedais', blank=True)

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'

    def __str__(self):
        return self.nome

    def slugfy(self, nome):
        from unicodedata import normalize
        sem_acento = normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
        return sem_acento.replace(' ', '-').lower()

    def save(self, *args, **kwargs):
        self.slug = self.slugfy(self.nome)
        super(Grupos, self).save(*args, **kwargs) # Call the real save() method
        

class Pedal(models.Model):
    objects = models.Manager()

    grupo = models.ForeignKey('Grupos',  on_delete=models.CASCADE, verbose_name='Grupo')
    data = models.DateField('Data', blank=True, null=True)   
    hora = models.TimeField('Hora', blank=True, null=True)
    concentracao = models.CharField('Encontro', max_length=25)
    quilometragem = models.DecimalField('Quilometragem', max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    destino = models.CharField('Destino', max_length=25)
    info = models.TextField('Informações Adicinais')

    niveis = (
        ('1', 'Iniciante'),
        ('1', 'Médio'),
        ('1', 'Avançado'),
    )
    nivel = models.CharField('Nível de dificuldade', max_length=1, choices=niveis)
    
    terrenos = (
        ('1', 'Terra'),
        ('2', 'Asfalto'),
        ('3', 'Misto'),
    )
    terreno = models.CharField('Terreno', max_length=1, choices=terrenos)

    criacao = models.DateTimeField('Criado em', auto_now_add=True)
    modificacao = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Pedal'
        verbose_name_plural = 'Pedais'

    def __str__(self):
        return 'Pedal de {} - {}'.format(self.data, self.destino)
