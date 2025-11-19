from django.contrib import admin
from .models import Mensaje, Conversacion
# Register your models here.

class MensajeAdmin(admin.ModelAdmin):
    list_display = ('conversacion', 'autor', 'texto', 'creado')
    list_filter = ('conversacion', 'autor')
    search_fields = ('texto',)

class MensajeInline(admin.TabularInline):
    model = Mensaje
    extra = 0
    fields = ('autor', 'texto', 'creado')
    readonly_fields = ('creado',)

class ConversacionAdmin(admin.ModelAdmin):
    list_display = ('producto', 'comprador', 'vendedor', 'creada')
    inlines = [MensajeInline]


admin.site.register(Mensaje, MensajeAdmin)
admin.site.register(Conversacion, ConversacionAdmin)