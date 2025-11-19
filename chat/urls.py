from django.urls import path
from . import views

urlpatterns = [
    path('abrir/<int:producto_id>/', views.abrir_chat, name='abrir_chat'),
    path('room/<int:conversacion_id>/', views.chat_room, name='chat_room'),
]
