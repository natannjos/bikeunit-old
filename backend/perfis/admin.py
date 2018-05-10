from django.contrib import admin
from .models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['amigos',
                       'convites_recebidos',
                       'convites_enviados',
                       'meus_grupos',
                       'pedais_gratis',
                       'pedais_agendados',
                       ]


admin.site.register(Profile, ProfileAdmin)
