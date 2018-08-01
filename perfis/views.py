from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Profile
from grupos.models import Pedal, SolicitacaoParticipacaoDePedal, TipoDeSolicitacao

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from django.urls import reverse_lazy


class SairDePedal(LoginRequiredMixin, TemplateView):

    template_name = 'perfis/includes/parcial_perfil_sair_pedal_update.html'
    model = Pedal

    def get_object(self):
        pk = self.kwargs['pk']
        try:
            pedal = Pedal.objects.get(pk=pk)
        except:
            pedal = None
        return pedal

    def get(self, request, *args, **kwargs):
        super(SairDePedal, self).get(request, *args, **kwargs)
        if request.is_ajax():
            data = {}
            pedal = self.get_object()
            data['html_form'] = render_to_string(
                self.template_name,
                {'pedal': pedal},
                request=request
            )
            return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        try:
            pedal = self.get_object()
            request.user.profile.pedais_agendados.remove(pedal)
            pedal.participantes.remove(request.user.profile)
        except:
            pass

        data = {}

        pedais = request.user.profile.pedais_agendados.all()
        if request.user.profile.pedais_agendados.count() == 0:
            data['tem_pedais'] = False
        else:
            data['tem_pedais'] = True
        data['html_pedais_agendados_list'] = render_to_string(
            'core/includes/lista_pedais_agendados_home.html', {
                'pedais_agendados': pedais
            })

        return JsonResponse(data)


class EntrarEmPedal(LoginRequiredMixin, TemplateView):

    template_name = 'perfis/entrar_em_pedal.html'

    def get_object(self):
        pk = self.kwargs['pk']

        try:
            pedal = Pedal.objects.get(pk=pk)
        except:
            pedal = None
        return pedal

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}
            pedal = self.get_object()
            if pedal:
                if request.user in pedal.grupo.participantes.all():
                    pedal.participantes.add(request.user.profile)
                    request.user.profile.pedais_agendados.add(pedal)
                else:
                    SolicitacaoParticipacaoDePedal.objects.create(
                        criador_convite_pedal=request.user.profile,
                        pedal=pedal,
                        convidado_ou_solicitante_pedal=request.user,
                        tipo=TipoDeSolicitacao.PEDIDO
                    )

            return JsonResponse(data)


entrar_em_pedal = EntrarEmPedal.as_view()
sair_de_pedal = SairDePedal.as_view()
