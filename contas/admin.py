from django.contrib import admin
from .models import User
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .forms import UserAdminCreationForm, UserAdminForm

# Register your models here.

class UserAdmin( admin.ModelAdmin ):
    # add_fieldsets = (
    #     (None, {
    #         'fields': ('username', 'email', 'password1', 'password2')
    #     }),
    # )
    # form = UserAdminForm
    # fieldsets = (
    #     (None, {
    #         'fields': ('username', 'email', 'token')
    #     }),
    #     ('Informações Pessoais', {
    #         'fields': (
    #             'telefone',
    #             'tel_emergencia',
    #             'sexo',
    #             'nascimento',
    #             'cpf',
    #             'password',
    #             'idade'

    #         )
    #     }),
    #     ('Endereço', {
    #         'fields': (
    #             'cep',
    #             'rua',
    #             'bairro',
    #             'cidade',
    #             'estado',
    #         )
    #     }
    #     ),
    #     ('Social',
    #         {
    #             'fields':(
    #                 'amigos',
    #                 'convites_recebidos',
    #                 'convites_enviados',
    #             )
    #         }
    #     ),
        
    #     ('Pedais e Grupos',
    #         {
    #             'fields':(
    #                 'meus_grupos',
    #                 'pedais_gratis',
    #                 'pedais_agendados',
    #                 'historico_de_pedais',
    #             )
    #         }
    #     ),
        
    #     ('Permissões', {
    #         'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'groups', 'user_permissions')
    #     }),
    # )
    # list_display = ['username', 'email', 'idade', 'is_active', 'is_staff',
    #                 'is_admin', 'date_joined']
    # list_filter = ['is_admin']
    readonly_fields = ('last_login', 'password', 'token')
    search_fields = ('username', 'email')


admin.site.register(User, UserAdmin)
