from rest_framework.exceptions import APIException

class ProfileDoesNotExist(APIException):
    status_code = 400
    default_detail = 'O perfil solicitado não existe'