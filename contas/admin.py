from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserAdminCreationForm, UserAdminForm

# Register your models here.

class UserAdmin( BaseUserAdmin ):
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )
    form = UserAdminForm
    fieldsets = (
        (None, {
            'fields': ('username', 'email')
        }),
        ('Informações Pessoais', {
            'fields': (
                'telefone',
                'tel_emergencia',
                'sexo',
                'nascimento',
                'cpf',
                'password',
                'idade'
            )
        }),
        ('Endereço', {
            'fields': (
                'cep',
                'rua',
                'bairro',
                'cidade',
                'estado',
            )
        }
        ),
        ('Social',
            {
                'fields':(
                    'amigos',
                    'convites_recebidos',
                    'convites_enviados',
                )
            }
        ),
        
        ('Pedais e Grupos',
            {
                'fields':(
                    'meus_grupos',
                    'pedais_gratis',
                )
            }
        ),
        
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'groups', 'user_permissions')
        }),
    )
    list_display = ['username', 'email', 'idade', 'is_active', 'is_staff',
                    'is_admin', 'date_joined']
    list_filter = ['is_admin']
    readonly_fields = ('last_login', 'password', 'idade', 'amigos', 'convites_enviados', 'convites_recebidos')
    search_fields = ('username', 'email')


admin.site.register(User, UserAdmin)
