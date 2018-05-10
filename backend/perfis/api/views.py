from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from perfis.models import Profile
from perfis.api.renderers import ProfileJSONRenderer
from perfis.api.serializers import ProfileSerializer
from perfis.api.exceptions import ProfileDoesNotExist
from django.core.exceptions import ObjectDoesNotExist

class ProfileRetrieveAPIView(RetrieveAPIView):

    permission_classes = (AllowAny, )
    renderer_classes = (ProfileJSONRenderer, )
    serializer_class = ProfileSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        try:
            profile = Profile.objects.select_related('user').get(
                user__pk=pk)
        except ObjectDoesNotExist:
            raise ProfileDoesNotExist

        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)
