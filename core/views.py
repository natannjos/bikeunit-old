from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from grupos.models import Grupos

class Home(LoginRequiredMixin, TemplateView):

    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)

        user = self.request.user

        grupos_da_cidade = Grupos.objects.filter(cidade=user.profile.cidade, estado=user.profile.estado)

        context['range'] = range(4)
       
        context['grupos_da_cidade'] = grupos_da_cidade
        return context

class Contato(TemplateView):
    template_name = 'core/contato.html'

home = Home.as_view()
contato = Contato.as_view()