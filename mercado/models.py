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

class Pago(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]

    TARJETA_CHOICES = [
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('amex', 'American Express'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_tarjeta = models.CharField(max_length=20, choices=TARJETA_CHOICES)
    ultimos_digitos = models.CharField(max_length=4)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    transaction_id = models.CharField(max_length=100, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Pago {self.transaction_id} - {self.estado}"