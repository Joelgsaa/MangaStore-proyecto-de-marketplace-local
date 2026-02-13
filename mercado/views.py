from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import Usuario, Producto, Carrito, Pago
from .serializers import UsuarioSerializer, ProductoSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductoFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import mercadopago
from django.conf import settings
from django.http import JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
import random
from django.utils import timezone

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductoFilter
# Create your views here.

# mostrar los productos

@login_required
def productos_list(request):
    productos = Producto.objects.all()
    return render(request, 'mercado/productos.html', {'productos': productos})

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'mercado/registro.html', {'form': form})

def productos_list(request):
    query = request.GET.get('q')
    productos = Producto.objects.all()
    if query:
        productos = productos.filter(titulo__icontains=query)
    return render(request, 'mercado/productos_list.html', {'productos': productos})

def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'mercado/producto_detalle.html', {'producto': producto})


@login_required
def ver_carrito(request):
    items = Carrito.objects.filter(usuario=request.user)
    total = sum(item.producto.precio * item.cantidad for item in items)
    return render(request, 'mercado/carrito.html', {'items': items, 'total': total})

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Verificar si ya está en el carrito
    item, creado = Carrito.objects.get_or_create(
        usuario=request.user,
        producto=producto,
        defaults={'cantidad': 1}
    )

    if not creado:
        item.cantidad += 1
        item.save()

    return redirect('productos_list')

def eliminar_del_carrito(request, producto_id):
    item = get_object_or_404(Carrito, producto_id=producto_id, usuario=request.user)
    item.delete()
    return redirect('ver_carrito')

def create_preference(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        raise Http404("Producto no encontrado")

    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    preference_data = {
        "items": [{
            "title": producto.titulo,
            "quantity": 1,
            "unit_price": float(producto.precio),
            "currency_id": "ARS",
        }],
        "back_urls": {
            "success": request.build_absolute_uri("/pago-exitoso/"),
            "failure": request.build_absolute_uri("/pago-fallido/"),
            "pending": request.build_absolute_uri("/pago-pendiente/"),
        },
        "auto_return": "approved",
    }

    preference = sdk.preference().create(preference_data)
    return JsonResponse({"init_point": preference["response"]["init_point"]})

@csrf_exempt
def mercadopago_webhook(request):
    # procesar notificación
    return HttpResponse(status=200)

def crear_preferencia(request, producto_id):
    producto = Producto.objects.get(id=producto_id)

    sdk = mercadopago.SDK("TU_ACCESS_TOKEN")

    preference_data = {
        "items": [
            {
                "title": producto.titulo,
                "quantity": 1,
                "unit_price": float(producto.precio),
            }
        ],
        "back_urls": {
            "success": "http://127.0.0.1:8000/success/",
            "failure": "http://127.0.0.1:8000/failure/",
            "pending": "http://127.0.0.1:8000/pending/"
        },
        "auto_return": "approved",
    }

    preference_response = sdk.preference().create(preference_data)
    return JsonResponse({"id": preference_response["response"]["id"]})

# simular_pago
def pago(request):
    """Página con formulario de pago simulado"""
    items = Carrito.objects.filter(usuario=request.user)
    total = sum(item.producto.precio * item.cantidad for item in items)
    
    if not items:
        return redirect('ver_carrito')
    
    return render(request, 'mercado/pago_simulado.html', {
        'items': items,
        'total': total
    })

@csrf_exempt
def procesar_pago(request):
    """Procesa el pago simulado"""
    if request.method == 'POST':
        try:
            numero_tarjeta = request.POST.get('numero_tarjeta', '').replace(' ', '')
            cvv = request.POST.get('cvv')
            vencimiento = request.POST.get('vencimiento')
            nombre_titular = request.POST.get('nombre_titular')
            
            # Validar tipo de tarjeta
            if numero_tarjeta.startswith('4'):
                tipo_tarjeta = 'visa'
            elif numero_tarjeta.startswith('5'):
                tipo_tarjeta = 'mastercard'
            elif numero_tarjeta.startswith('3'):
                tipo_tarjeta = 'amex'
            else:
                tipo_tarjeta = 'desconocida'
            
            # Determinar estado (90% aprobado, 10% rechazado para simulación)
            # Para forzar rechazo usar tarjeta que termine en 0000
            if numero_tarjeta.endswith('0000'):
                estado = 'rechazado'
            else:
                estado = random.choices(['aprobado', 'rechazado'], weights=[90, 10])[0]
            
            # Calcular total
            items = Carrito.objects.filter(usuario=request.user)
            total = sum(item.producto.precio * item.cantidad for item in items)
            
            # Generar transaction_id
            transaction_id = f"SIM-{uuid.uuid4().hex[:12].upper()}"
            
            # Guardar pago
            pago = Pago.objects.create(
                usuario=request.user,
                monto=total,
                tipo_tarjeta=tipo_tarjeta,
                ultimos_digitos=numero_tarjeta[-4:],
                estado=estado,
                transaction_id=transaction_id
            )
            
            # Si fue aprobado, limpiar carrito
            if estado == 'aprobado':
                items.delete()
                return redirect('pago_exitoso', pago_id=pago.id)
            else:
                return render(request, 'mercado/pago_rechazado.html', {
                    'pago': pago,
                    'razon': 'Tarjeta rechazada por el banco emisior'
                })
                
        except Exception as e:
            return render(request, 'mercado/pago_error.html', {'error': str(e)})
    
    return redirect('ver_carrito')

def pago_exitoso(request, pago_id):
    """Página de pago exitoso"""
    pago = get_object_or_404(Pago, id=pago_id, usuario=request.user)
    return render(request, 'mercado/pago_exitoso.html', {'pago': pago})

def historial_pagos(request):
    """Ver historial de pagos del usuario"""
    pagos = Pago.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'mercado/historial_pagos.html', {'pagos': pagos})