from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView
from django.utils.safestring import mark_safe
import json
from .models import Room
from django.contrib.auth.mixins import LoginRequiredMixin

class New_Room(LoginRequiredMixin, CreateView):
    model = Room
    template_name = 'chat/index.html'
    fields = ['name']

    def form_valid(self, form):
        room_name = form.instance.name
        if room_name in [map(lambda x: x.name, Room.objects.all())]:
            return redirect(Room.objects.get(name=room_name).get_absolute_url())
        
        return super(New_Room, self).form_valid(form)

class Chat_Room(LoginRequiredMixin, TemplateView):
    template_name = 'chat/room.html'

    def get_context_data(self, **kwargs):
        room = Room.objects.get_or_create(label=kwargs.get('label'))[0]

        messages = room.messages.order_by('created')[:50]
        context = super(Chat_Room, self).get_context_data(**kwargs)

        context['room_name_json'] = mark_safe(json.dumps(kwargs.get('label')))
        context['messages'] = messages
        context['room'] = room

        return context


index = New_Room.as_view()
room = Chat_Room.as_view()
