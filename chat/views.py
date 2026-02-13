from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Conversacion, Mensaje
from mercado.models import Producto


def abrir_chat(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    vendedor = producto.vendedor
    comprador = request.user

    if vendedor == comprador:
        return redirect('producto_detalle', pk=producto_id)

    conversacion, _ = Conversacion.objects.get_or_create(
        producto=producto,
        comprador=comprador,
        vendedor=vendedor
    )
    return redirect('chat_room', conversacion_id=conversacion.id)


def chat_room(request, conversacion_id):
    conversacion = get_object_or_404(Conversacion, id=conversacion_id)
    if request.user.id not in (conversacion.comprador_id, conversacion.vendedor_id):
        return redirect('productos_list')

    mensajes = conversacion.mensajes.select_related('autor').all()
    return render(request, 'chat/room.html', {'conversacion': conversacion, 'mensajes': mensajes})


def lista_conversaciones(request):
    conversaciones = Conversacion.objects.filter(
        Q(comprador=request.user) | Q(vendedor=request.user)
    ).prefetch_related('mensajes', 'producto').order_by('-creada')

    for c in conversaciones:
        c.mensajes_no_leidos = c.mensajes.filter(
            creado__gte=timezone.now() - timedelta(days=7)
        ).count()

    return render(request, 'chat/conversaciones.html', {'conversaciones': conversaciones})
