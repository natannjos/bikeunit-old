from rest_framework import serializers

from perfis.models import Profile

class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile

        fields = [
            'pk',
            'username',
            'image',
            'nascimento',
            'telefone',
            'tel_emergencia',
            'cpf',
            'is_admin'
            ]

        read_only_fields = ['username', ]
    def get_image(self, obj):
        if obj.image:
            return obj.image
        return 'https://static.productionready.io/images/smiley-cyrus.jpg'
