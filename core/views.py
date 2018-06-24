from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from grupos.models import Grupos
from django.http import HttpResponseForbidden

from django.db.models import Count


class BuscaGruposLocalidadeAjax(LoginRequiredMixin, ListView):

    template_name = 'core/buscas/busca_por_cidade.html'
    model = Grupos
    paginate_by = 10
    context_object_name = 'grupos_da_cidade'

    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax():
            return super(BuscaGruposLocalidadeAjax, self).dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()
    

    def get_queryset(self):
        queryset = super(BuscaGruposLocalidadeAjax, self).get_queryset()
        user = self.request.user
        if self.request.GET.get('primeira'):
            queryset = Grupos.objects.filter(
                cidade=user.profile.cidade, estado=user.profile.estado, publico=True).annotate(num_pedais=Count('pedais')).order_by('-num_pedais')
        else:
            queryset = Grupos.objects.filter(cidade=self.request.GET.get(
                'cidade'), publico=True).annotate(num_pedais=Count('pedais')).order_by('-num_pedais')

        return queryset

    def get_context_data(self, **kwargs):
        context = super(BuscaGruposLocalidadeAjax, self).get_context_data(**kwargs)

        context['cidade'] = self.request.user.profile.cidade
        if self.request.is_ajax:
            context['cidade'] = self.request.GET.get('cidade')

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
