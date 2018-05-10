import json

from rest_framework.renderers import JSONRenderer
from core.api.renderers import BikeUnitJSONRenderer

class UserJSONRenderer(BikeUnitJSONRenderer):
    object_label = 'user'

    def render(self, data, media_type=None, renderer_context=None):

        # If we receive a `token` key as part of the response, it will be a
        # byte object. Byte objects don't serialize well, so we need to
        # decode it before rendering the User object.
        token = data.get('token', None)

        
        if token is not None and isinstance(token, bytes):
            # Also as mentioned above, we will decode `token` if it is of type
            # bytes.
            data['token'] = token.decode('utf-8')

        return super(UserJSONRenderer, self).render(data)
