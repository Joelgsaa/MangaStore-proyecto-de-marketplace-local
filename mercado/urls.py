from django.urls import path
from . import views
from .views import productos_list
from django.contrib.auth import views as auth_views
from mercado.views import mercadopago_webhook


urlpatterns = [
    path('', productos_list, name='productos_list'),
    path('login/', auth_views.LoginView.as_view(template_name='mercado/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('productos/', views.productos_list, name='productos_list'),
    path('producto/<int:pk>/', views.producto_detalle, name='producto_detalle'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path("pago/<int:producto_id>/", views.create_preference, name="crear-preferencia"),
    path("webhooks/mercadopago/", mercadopago_webhook, name="mercadopago_webhook"),
    path('crear_preferencia/<int:producto_id>/', views.crear_preferencia, name='crear_preferencia'),
]

# por las dudas: from .views import productos_list, registro