from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    reputacion = models.FloatField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Producto(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    demografia = models.CharField(max_length=100, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE) # vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

