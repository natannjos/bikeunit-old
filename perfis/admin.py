from django.contrib import admin
from .models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['meus_grupos',
                       'pedais_agendados',
                       ]


admin.site.register(Profile, ProfileAdmin)
