from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User

class RegistroDeUsuarioView(CreateView):

    model = User
    

