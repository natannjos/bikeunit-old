from django.contrib import admin

from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('core.urls',  namespace='core')),
    path('login/', auth_views.login, {'template_name': 'login/login.html',
                                'redirect_authenticated_user': True}, name='login'),
    path('sair/', auth_views.logout_then_login, name='logout'),

    path('api/autenticacao/', include('contas.api.urls', namespace='api_auth')),
    path('api/', include('perfis.api.urls', namespace='profiles'))
]