from django.contrib import admin
from .models import Grupos, Pedal


# Register your models here.
class GruposAdmin(admin.ModelAdmin):   

    readonly_fields = ('criacao', 'modificacao', 'slug')

    list_display = ['nome', 'slug',  'estado', 'cidade']
    list_filter = ['nome', 'slug', 'admin', 'estado', 'cidade']
    search_fields = ['nome', 'slug', 'admin', 'estado', 'cidade']

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
