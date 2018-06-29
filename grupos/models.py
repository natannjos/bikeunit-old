from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.conf import settings

from localflavor.br.br_states import STATE_CHOICES
from localflavor.br.models import BRStateField
from perfis.models import Profile

from django.db import transaction
from decimal import Decimal

# Create your models here.
class Grupos(models.Model):
    objects = models.Manager()

    admin = models.ManyToManyField(settings.AUTH_USER_MODEL,
                              verbose_name='Administradores', related_name='admin')

    nome = models.CharField('Nome do grupo', max_length=20, unique=True)
    capa = models.ImageField('Capa', blank=True, null=True, upload_to='grupos/capas')
    logo = models.ImageField('Logo', blank=True, null=True, upload_to='grupos/logos')
    slug = models.SlugField()
    criacao = models.DateTimeField('Criado em', auto_now_add=True)
    modificacao = models.DateTimeField('Modificado em', auto_now=True)
    
    estado = BRStateField('Estado', choices=STATE_CHOICES, max_length=2, blank=True, null=True)
    cidade = models.CharField('Cidade', max_length=50, blank=True)

    participantes = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Participantes', blank=True, related_name='participantes')
    pedais = models.ManyToManyField('grupos.Pedal', verbose_name='Pedais', blank=True)

    publico = models.BooleanField('Público', default=True)
    convites_enviados = models.ManyToManyField(
        'ConviteDeGrupo', verbose_name='Convites Enviados', related_name='convites_enviados', blank=True)
    convites_aguardando_aprovacao = models.ManyToManyField('ConviteDeGrupo', verbose_name='Convites Aguardando Aprovação', related_name='convites_aguardando_aprovacao', blank=True)

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

    @property
    def pedais_ativos(self):
        return self.pedais.filter(ativo=True).order_by('-modificacao')
    
    @property
    def realizados(self):
        return self.pedais.filter(ativo=False).order_by('-criacao')

def add_grupo_a_lista_de_grupos_do_admin(instance):
    for user in instance.admin.all():
        perfil = Profile.objects.get(user=user)
        perfil.meus_grupos.add(instance)
        perfil.id_admin = True
        perfil.save()
        instance.participantes.add(user)

def atualiza_membros_apos_commit(instance, **kwargs):
    transaction.on_commit(
        lambda: add_grupo_a_lista_de_grupos_do_admin(instance))

models.signals.post_save.connect(
    atualiza_membros_apos_commit, sender=Grupos, dispatch_uid='atualizaparticipantes_apos_commit'
)

class ConviteDeGrupo(models.Model):
    objects = models.Manager()
    criador = models.ForeignKey('perfis.Profile',
                                related_name='criador_do_convite',
                                on_delete=models.SET_NULL,
                                verbose_name="Quem convidou",
                                null=True
                                )
    grupo_que_convidou = models.ForeignKey('Grupos', related_name='grupo_que_convidou', on_delete=models.CASCADE, verbose_name='Grupo que convidou')
    convidado = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='convidado', on_delete=models.CASCADE, verbose_name='Convidado')
    
    PENDENTE = 0
    ACEITO = 1
    APROVADO = 2
    REGEITADO = 3
    status_choices = (
        (PENDENTE, 'Pendente'),
        (ACEITO, 'Aceito'),
        (APROVADO, 'Aprovado'),
        (REGEITADO, 'Regeitado'),
    )

    status = models.SmallIntegerField('Status', choices=status_choices, default=PENDENTE)
    criacao = models.DateTimeField('Criação', auto_now_add=True)

    class Meta:
        verbose_name = 'Convite de Grupo'
        verbose_name_plural = 'Convites de Grupo'

    def __str__(self):
        return '{} convida {} para {}'.format(self.criador, self.convidado, self.grupo_que_convidou)


def adiciona_convite_a_lista_do_usuario_e_do_grupo(convite):
    convite.convidado.profile.convites_de_grupo_recebidos.add(convite)
    convite.grupo_que_convidou.convites_enviados.add(convite)

def adiciona_convite_a_lista_aguardamdo_aprovacao(convite):
    convite.grupo_que_convidou.convites_aguardando_aprovacao.add(convite)

def adiciona_usuario_ao_grupo(convite):
    convite.grupo_que_convidou.participantes.add(convite.convidado)
    convite.convidado.profile.meus_grupos.add(convite.grupo_que_convidou)
    convite.delete()

def adiciona_usuario_ao_grupo_apos_confirmacao(instance, created, **kwargs):
    if created:
        transaction.on_commit(
            lambda: adiciona_convite_a_lista_do_usuario_e_do_grupo(instance))

    if instance.criador.is_admin and instance.status == ConviteDeGrupo.ACEITO:
        transaction.on_commit(
            lambda: adiciona_usuario_ao_grupo(instance)
        )
        return

    if instance.status == ConviteDeGrupo.ACEITO:
        transaction.on_commit(
            lambda: adiciona_convite_a_lista_aguardamdo_aprovacao(instance))

    if instance.status == ConviteDeGrupo.APROVADO:
         transaction.on_commit(
             lambda: adiciona_usuario_ao_grupo(instance)
         )
         return 

    if instance.status == ConviteDeGrupo.REGEITADO:
        instance.delete()
    

models.signals.post_save.connect(
    adiciona_usuario_ao_grupo_apos_confirmacao, sender=ConviteDeGrupo, dispatch_uid='adiciona_usuario_ao_grupo_apos_confirmacao'
)

class Pedal(models.Model):
    objects = models.Manager()
    criador = models.ForeignKey('perfis.Profile', 
        related_name='criador', 
        on_delete=models.SET_NULL, 
        verbose_name='Criador', 
        limit_choices_to={'is_admin':True},
        null=True)

    grupo = models.ForeignKey('Grupos',  on_delete=models.CASCADE, verbose_name='Grupo')
    data = models.DateField('Data', blank=True, null=True)   
    hora = models.TimeField('Hora', blank=True, null=True)
    concentracao = models.CharField('Encontro', max_length=25)
    quilometragem = models.DecimalField('Quilometragem', max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    destino = models.CharField('Destino', max_length=25)
    info = models.TextField('Informações Adicinais')
    publico = models.BooleanField('Público', default=False)
    pago = models.BooleanField('Pedal Pago', default=False)
    preco = models.DecimalField('Preço', max_digits=8, decimal_places=2, default=Decimal(0.0))
    participantes = models.ManyToManyField('perfis.Profile', verbose_name="Participantes", related_name='participantes', blank=True)
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
    ativo = models.BooleanField('Ativo', default=True)
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Pedal'
        verbose_name_plural = 'Pedais'

    def __str__(self):
        return 'Pedal de {} - {}'.format(self.data, self.destino)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('grupos:grupo_info', kwargs={'slug': self.slug})


def atualiza_modelos_apos_commit(instance, created):
    if created:
        instance.participantes.add(instance.criador)
        instance.criador.pedais_agendados.add(instance)
    
    instance.grupo.pedais.add(instance)

def add_criador_em_participantes(instance, created, **kwargs):
    transaction.on_commit(
        lambda: atualiza_modelos_apos_commit(instance, created)
    )

models.signals.post_save.connect(
    add_criador_em_participantes, sender=Pedal, dispatch_uid='add_criador_em_participantes'
)
