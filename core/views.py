from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from grupos.models import Grupos

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class BuscaGruposLocalidadeAjax(LoginRequiredMixin, TemplateView):
    
    template_name = 'core/buscas/pedais_grande.html'

    def get_context_data(self, **kwargs):
        context = super(BuscaGruposLocalidadeAjax, self).get_context_data(**kwargs)

        user = self.request.user
        if self.request.is_ajax():
            context['grupos_da_cidade'] = Grupos.objects.filter(cidade=self.request.GET.get('cidade'), publico=True)
            context['cidade'] = self.request.GET.get('cidade')
        else:
            context['grupos_da_cidade'] = Grupos.objects.filter(cidade=user.profile.cidade, estado=user.profile.estado, publico=True)

        return context

class Home(LoginRequiredMixin, TemplateView):

    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)

        user = self.request.user
        context['meus_grupos'] = user.profile.meus_grupos.all()
        context['pedais_agendados'] = user.profile.pedais_agendados.all()
        
        return context

class Contato(TemplateView):
    template_name = 'core/contato.html'



home = Home.as_view()
contato = Contato.as_view()
busca_grupo_por_localidade = BuscaGruposLocalidadeAjax.as_view()
