from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from pusher import Pusher
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse

try:
    import bikeapp.local_settings
    ssl = False
except ImportError:
    ssl= True

pusher = Pusher(
    app_id='533241',
    key='9e1445ca72ab1228b6c6',
    secret='fa4c120420de83455d40',
    cluster='us2',
    ssl=ssl
)

class Chat(LoginRequiredMixin, TemplateView):
    login_url = '/admin/login/'
    template_name = 'chat/chat.html'

@csrf_exempt
def broadcast(request, *args, **kwargs):
    pusher.trigger('my_channel', 'my_event', {'name': request.user.username, 'message': request.POST['message']})
    return HttpResponse('done')
