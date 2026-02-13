from django.contrib import admin
from .models import Usuario, Producto, Carrito, Pago

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Carrito)

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'usuario', 'monto', 'tipo_tarjeta', 'estado', 'fecha']
    list_filter = ['estado', 'tipo_tarjeta', 'fecha']
    search_fields = ['transaction_id', 'usuario__username']
    readonly_fields = ['transaction_id', 'fecha']