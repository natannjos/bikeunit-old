from django.contrib import admin

from django.urls import path, include
from django.contrib.auth import views as auth_views

from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import views, serializers, status
from rest_framework.response import Response


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class EchoView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('core.urls',  namespace='core')),
    path('login/', auth_views.login, {'template_name': 'login/login.html',
                                'redirect_authenticated_user': True}, name='login'),
    path('sair/', auth_views.logout_then_login, name='logout'),

    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', get_schema_view()),
    path('api/auth/token/obtain/', TokenObtainPairView.as_view()),
    path('api/auth/token/refresh/', TokenRefreshView.as_view()),
    path('api/echo/', EchoView.as_view())

]
