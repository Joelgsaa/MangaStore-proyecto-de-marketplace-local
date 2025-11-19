from django.shortcuts import render, get_object_or_404, redirect
from .models import Conversacion
from mercado.models import Producto

# Create your views here.
def abrir_chat(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    vendedor = producto.vendedor  # ajustá al campo del vendedor
    comprador = request.user
    conversacion, _ = Conversacion.objects.get_or_create(
        producto=producto,
        comprador=comprador,
        vendedor=vendedor
    )
    return redirect('chat_room', conversacion_id=conversacion.id)

def chat_room(request, conversacion_id):
    from .models import Mensaje
    conversacion = get_object_or_404(Conversacion, id=conversacion_id)
    # Seguridad: solo participantes
    if request.user.id not in (conversacion.comprador_id, conversacion.vendedor_id):
        return redirect('productos_lista')
    mensajes = conversacion.mensajes.select_related('autor').all()
    return render(request, 'chat/room.html', {'conversacion': conversacion, 'mensajes': mensajes})
