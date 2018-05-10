from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class Home(LoginRequiredMixin, TemplateView):

    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['range'] = range(4)
        return context


home = Home.as_view()
