from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Grupos

class GruposAdminLista(LoginRequiredMixin, TemplateView):

    template_name = 'grupos/lista-grupos-admin.html'


    def get_context_data(self, **kwargs):
        context = super(GruposAdminLista, self).get_context_data(**kwargs)
        context['meus_grupos'] = Grupos.objects.filter(admin=self.request.user)
        return context


grupos_admin_lista = GruposAdminLista.as_view()
