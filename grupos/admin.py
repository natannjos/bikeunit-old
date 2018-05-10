from django.contrib import admin
from .models import Grupos, Pedal


# Register your models here.
class GruposAdmin(admin.ModelAdmin):   

    list_display = ['nome', 'criacao', 'modificacao']
    list_filter = ['nome', 'admin']
    readonly_fields = ('criacao', 'modificacao', 'slug')
    search_fields = ('nome', 'admin')


class PedalAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'grupo', 'data', 'hora', 'nivel', 'terreno']
    list_filter = ['grupo', 'data', 'destino', 'nivel', 'terreno', 'quilometragem']
    readonly_fields = ('criacao', 'modificacao')
    search_fields = (
        'grupo',
        'concentracao',
        'quilometragem',
        'destino',
        'nivel',
        'terreno',
    )
    
admin.site.register(Grupos, GruposAdmin)
admin.site.register(Pedal, PedalAdmin)
