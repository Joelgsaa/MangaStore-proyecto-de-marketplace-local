from django.contrib import admin
from .models import Usuario, Producto, Carrito

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Carrito)