from django.db import models
from django.conf import settings
from mercado.models import Producto


# Create your models here.
class Conversacion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='conversaciones')
    comprador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversaciones_comprador')
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversaciones_vendedor')
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('producto', 'comprador', 'vendedor')

    def __str__(self):
        return f"{self.producto.titulo} — {self.comprador} ↔ {self.vendedor}"

class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['creado']
