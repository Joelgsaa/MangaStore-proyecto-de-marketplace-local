from django.core.management.base import BaseCommand
from mercado.models import Producto

import cloudinary.uploader

class Command(BaseCommand):
    help = "Sube imágenes de productos a Cloudinary y actualiza la base de datos"

    def handle(self, *args, **kwargs):
        for producto in Producto.objects.all():
            if producto.imagen and producto.imagen.path:
                self.stdout.write(f"Subiendo imagen de: {producto.titulo}")
                result = cloudinary.uploader.upload(producto.imagen.path)
                producto.imagen = result['secure_url']
                producto.save()
                self.stdout.write(self.style.SUCCESS(f"Imagen subida y actualizada: {producto.titulo}"))