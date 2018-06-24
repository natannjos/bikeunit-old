from django.contrib import admin

from django.urls import path, include
from django.contrib.auth import views as auth_views
from chat.views import broadcast

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # URLs de funções gerais
    path('', include('core.urls',  namespace='core')),

    # URLs de Autenticação
    path('entrar/', auth_views.login, {'template_name': 'contas/login/login.html',
                                'redirect_authenticated_user': True}, name='login'),
    path('sair/', auth_views.logout_then_login, name='logout'),

    # URLs de APIs
    path('api/autenticacao/', include('contas.api.urls', namespace='api_auth')),
    path('api/', include('perfis.api.urls', namespace='profiles')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('ajax/chat/', broadcast),

    # URLs dos apps
    path('conta/', include('contas.urls', namespace='contas')),
    path('grupo/', include('grupos.urls', namespace='grupos'))

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )