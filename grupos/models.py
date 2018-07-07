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
        'SolicitacaoParticipacaoDeGrupo', verbose_name='Convites Enviados', related_name='convites_enviados', blank=True)
    solicitacoes_aguardando_aprovacao = models.ManyToManyField('SolicitacaoParticipacaoDeGrupo', verbose_name='Convites Aguardando Aprovação', related_name='solicitacoes_aguardando_aprovacao', blank=True)

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

# Signals de Grupo
def add_grupo_a_lista_de_grupos_do_admin(instance):
    for user in instance.admin.all():
        perfil = Profile.objects.get(user=user)
        perfil.meus_grupos.add(instance)
        perfil.is_admin = True
        perfil.save()
        instance.participantes.add(user)

def atualiza_membros_apos_commit(instance, **kwargs):
    transaction.on_commit(
        lambda: add_grupo_a_lista_de_grupos_do_admin(instance))

models.signals.post_save.connect(
    atualiza_membros_apos_commit, sender=Grupos, dispatch_uid='atualiza_membros_apos_commit'
)

class Status(object):
    PENDENTE = 0
    AGUARDANDO_APROVAÇÃO = 1
    APROVADO = 2
    REGEITADO = 3
    opcoes = (
        (PENDENTE, 'Pendente'),
        (AGUARDANDO_APROVAÇÃO, 'Aguardando Aprovação'),
        (APROVADO, 'Aprovado'),
        (REGEITADO, 'Regeitado'),
    )

class TipoDeSolicitacao(object):
    CONVITE = 0
    PEDIDO = 1

    choices = (
        (CONVITE, 'Convite'),
        (PEDIDO, 'Pedido'),
    )

class SolicitacaoParticipacaoDeGrupo(models.Model):
    objects = models.Manager()
    criador = models.ForeignKey('perfis.Profile',
                                related_name='criador_do_convite',
                                on_delete=models.SET_NULL,
                                verbose_name="Quem convidou",
                                null=True
                                )
    grupo = models.ForeignKey('Grupos', related_name='grupo_alvo', on_delete=models.CASCADE, verbose_name='Grupo')
    convidado_ou_solicitante_grupo = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='convidado_ou_solicitante_grupo', on_delete=models.CASCADE, verbose_name='Convidado ou Solicitante')
    
    status = models.SmallIntegerField(
        'Status', choices=Status.opcoes, default=Status.PENDENTE)
    criacao = models.DateTimeField('Criação', auto_now_add=True)

    tipo = models.SmallIntegerField(
        'Tipo', 
        choices =TipoDeSolicitacao.choices
    )

    class Meta:
        verbose_name = 'Convite e Solicitação de Grupo'
        verbose_name_plural = 'Convites e Solicitações de Grupo'

    def __str__(self):
        if self.tipo == TipoDeSolicitacao.CONVITE:
            return '{} convida {} para {}'.format(self.criador, self.convidado_ou_solicitante_grupo, self.grupo)
        return '{} quer entrar no grupo {}'.format(self.convidado_ou_solicitante_grupo, self.grupo)

# signals de convite de grupo
def adiciona_convite_as_listas_do_usuario_e_do_grupo(solicitacao):
    if solicitacao.tipo == TipoDeSolicitacao.CONVITE:
        solicitacao.convidado_ou_solicitante_grupo.profile.convites_de_grupo_recebidos.add(
            solicitacao)
        solicitacao.grupo.convites_enviados.add(solicitacao)
    elif solicitacao.tipo == TipoDeSolicitacao.PEDIDO:
        solicitacao.convidado_ou_solicitante_grupo.profile.pedidos_participar_grupo.add(solicitacao)
        solicitacao.grupo.solicitacoes_aguardando_aprovacao.add(solicitacao)
        solicitacao.status = Status.AGUARDANDO_APROVAÇÃO
        solicitacao.save()

def adiciona_convite_a_lista_aguardando_aprovacao(solicitacao):
    solicitacao.grupo.solicitacoes_aguardando_aprovacao.add(solicitacao)

def adiciona_usuario_ao_grupo(solicitacao):
    solicitacao.grupo.participantes.add(solicitacao.convidado_ou_solicitante_grupo)
    solicitacao.convidado_ou_solicitante_grupo.profile.meus_grupos.add(
        solicitacao.grupo)
    solicitacao.delete()

def processa_solicitacao_de_grupo(instance, created, **kwargs):
    if created:
        transaction.on_commit(
            lambda: adiciona_convite_as_listas_do_usuario_e_do_grupo(instance))

    if (
        instance.criador.user in instance.grupo.admin.all() and
        instance.status == Status.AGUARDANDO_APROVAÇÃO and
        instance.tipo == TipoDeSolicitacao.CONVITE
    ):
        instance.status = Status.APROVADO

    if instance.status == Status.AGUARDANDO_APROVAÇÃO:
        transaction.on_commit(
            lambda: adiciona_convite_a_lista_aguardando_aprovacao(instance))

    if instance.status == Status.APROVADO:
         transaction.on_commit(
             lambda: adiciona_usuario_ao_grupo(instance)
         )
         return 

    if instance.status == Status.REGEITADO:
        instance.delete()

models.signals.post_save.connect(
    processa_solicitacao_de_grupo, 
    sender=SolicitacaoParticipacaoDeGrupo, 
    dispatch_uid='processa_solicitacao_de_grupo'
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

    convites_enviados = models.ManyToManyField(
        'SolicitacaoParticipacaoDePedal', verbose_name='Convites Enviados', related_name='convites_enviados', blank=True)
    solicitacoes_aguardando_aprovacao = models.ManyToManyField(
        'SolicitacaoParticipacaoDePedal', verbose_name='Solicitações Aguardando Aprovação', related_name='solicitacoes_aguardando_aprovacao', blank=True)

    class Meta:
        verbose_name = 'Pedal'
        verbose_name_plural = 'Pedais'

    def __str__(self):
        return 'Pedal de {} - {}'.format(self.data, self.destino)

    # def get_absolute_url(self):
    #     from django.core.urlresolvers import reverse
    #     return reverse('grupos:grupo_info', kwargs={'slug': self.slug})

# singlas de Pedal
def atualiza_modelos_apos_commit(instance, created):
    if created:
        instance.participantes.add(instance.criador)
        instance.criador.pedais_agendados.add(instance)
        instance.save()
    
    instance.grupo.pedais.add(instance)

def add_criador_em_participantes(instance, created, **kwargs):
    transaction.on_commit(
        lambda: atualiza_modelos_apos_commit(instance, created)
    )

models.signals.post_save.connect(
    add_criador_em_participantes, 
    sender=Pedal, 
    dispatch_uid='add_criador_em_participantes'
)


class SolicitacaoParticipacaoDePedal(models.Model):

    objects = models.Manager()
    criador_convite_pedal = models.ForeignKey('perfis.Profile',
                                related_name='criador_convite_pedal',
                                on_delete=models.SET_NULL,
                                verbose_name="Quem convidou",
                                null=True
                                )
    pedal = models.ForeignKey('Pedal', related_name='grupo_alvo', on_delete=models.CASCADE, verbose_name='Pedal', limit_choices_to={'ativo':True})
    convidado_ou_solicitante_pedal = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='convidado_ou_solicitante_pedal', on_delete=models.CASCADE, verbose_name='Convidado ou Solicitante')
    
    status = models.SmallIntegerField(
        'Status', choices=Status.opcoes, default=Status.PENDENTE)
    criacao = models.DateTimeField('Criação', auto_now_add=True)

    tipo = models.SmallIntegerField(
        'Tipo', 
        choices=TipoDeSolicitacao.choices
    )

    class Meta:
        verbose_name = 'Convite e Solicitação de Pedal'
        verbose_name_plural = 'Convites e Solicitações de Pedal'

    def __str__(self):
        if self.tipo == TipoDeSolicitacao.CONVITE:
            return '{} convida {} para  participar de {}'.format(self.criador_convite_pedal, self.convidado_ou_solicitante_pedal, self.pedal)
        return '{} quer participar do pedal {}'.format(self.convidado_ou_solicitante_pedal, self.pedal)


# Signals de convite de pedal

def adiciona_convite_as_listas_do_usuario_e_do_pedal(convite_pedal):
    if convite_pedal.tipo == TipoDeSolicitacao.CONVITE:
        convite_pedal.convidado_ou_solicitante_pedal.profile.convites_de_pedal_recebidos.add(convite_pedal)
        convite_pedal.pedal.convites_enviados.add(convite_pedal)

    elif convite_pedal.tipo == TipoDeSolicitacao.PEDIDO:
        convite_pedal.convidado_ou_solicitante_pedal.profile.pedidos_participar_pedal.add(convite_pedal)
        convite_pedal.pedal.solicitacoes_aguardando_aprovacao.add(convite_pedal)
        convite_pedal.status = Status.AGUARDANDO_APROVAÇÃO
        convite_pedal.save()

def adiciona_convite_a_lista_pedais_aguardando_aprovacao(convite_pedal):
    convite_pedal.pedal.solicitacoes_aguardando_aprovacao.add(convite_pedal)

def adiciona_usuario_ao_pedal(convite_pedal):
    convite_pedal.pedal.participantes.add(convite_pedal.convidado_ou_solicitante_pedal.profile)
    convite_pedal.convidado_ou_solicitante_pedal.profile.pedais_agendados.add(convite_pedal.pedal)
    convite_pedal.delete()

def processa_solicitacao_de_pedal(instance, created, **kwargs):
    if created:
        transaction.on_commit(
        lambda: adiciona_convite_as_listas_do_usuario_e_do_pedal(instance))

    if (
        instance.criador_convite_pedal.user in instance.pedal.grupo.admin.all() and
        instance.status == Status.AGUARDANDO_APROVAÇÃO and
        instance.tipo == TipoDeSolicitacao.CONVITE
    ):
        instance.status = Status.APROVADO

    if instance.status == Status.AGUARDANDO_APROVAÇÃO:
        transaction.on_commit(
            lambda: adiciona_convite_a_lista_pedais_aguardando_aprovacao(instance))

    if instance.status == Status.APROVADO:
         transaction.on_commit(
             lambda: adiciona_usuario_ao_pedal(instance)
         )
         return 

    if instance.status == Status.REGEITADO:
        instance.delete()
    

models.signals.post_save.connect(
    processa_solicitacao_de_pedal,
    sender=SolicitacaoParticipacaoDePedal,
    dispatch_uid='processa_solicitacao_de_pedal'
)
