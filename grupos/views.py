from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from .models import Grupos


class GruposAdminLista(LoginRequiredMixin, TemplateView):

    template_name = 'grupos/lista-grupos-admin.html'


    def get_context_data(self, **kwargs):
        u"""Adiciona os grupos que o usuário administra ao contexto."""
        context = super(GruposAdminLista, self).get_context_data(**kwargs)
        context['meus_grupos'] = Grupos.objects.filter(admin=self.request.user)

        return context


class GrupoInfo(LoginRequiredMixin, DetailView):

    template_name = 'grupos/tela-grupo.html'
    context_object_name = 'grupo'
    model = Grupos

    def dispatch(self, request, *args, **kwargs):
        u"""Checa se o usuário é admin do grupo escolhido."""
        """Se não for retorna um erro 403."""
        user = request.user
        grupo = self.get_object()
        if user.is_anonymous or user.profile.is_admin and user in grupo.admin.all():
            return super(GrupoInfo, self).dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()


grupos_admin_lista = GruposAdminLista.as_view()
grupo_info = GrupoInfo.as_view()
