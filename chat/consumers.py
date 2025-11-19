from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from .models import Conversacion, Mensaje

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversacion_id = self.scope['url_route']['kwargs']['conversacion_id']
        self.room_group_name = f"chat_{self.conversacion_id}"

        # Autorización: solo comprador o vendedor
        user = self.scope['user']
        allowed = await self.user_allowed(user, self.conversacion_id)
        if not user or isinstance(user, AnonymousUser) or not allowed:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        texto = data.get('texto', '').strip()
        if not texto:
            return

        user = self.scope['user']
        msg = await self.guardar_mensaje(user.id, self.conversacion_id, texto)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'mensaje_id': msg['id'],
                'autor': msg['autor'],
                'texto': msg['texto'],
                'creado': msg['creado'],
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def user_allowed(self, user, conversacion_id):
        try:
            c = Conversacion.objects.get(id=conversacion_id)
            return c.comprador_id == user.id or c.vendedor_id == user.id
        except Conversacion.DoesNotExist:
            return False

    @database_sync_to_async
    def guardar_mensaje(self, user_id, conversacion_id, texto):
        print(f"Intentando guardar mensaje: {texto} para user {user_id} y conversación {conversacion_id}")
        m = Mensaje.objects.create(
            conversacion_id=conversacion_id,
            autor_id=user_id,
            texto=texto
        )
        print(f"Mensaje guardado con ID: {m.id}")
        return {'id': m.id, 'autor': m.autor.username, 'texto': m.texto, 'creado': m.creado.isoformat()}
    