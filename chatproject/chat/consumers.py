# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Update user online status
        user = self.scope['user']
        if user.is_authenticated:
            await self.update_user_status(user, True)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # Update user online status
        user = self.scope['user']
        if user.is_authenticated:
            await self.update_user_status(user, False)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room_id = text_data_json['room_id']
        user = self.scope['user']
        
        if user.is_authenticated:
            # Save message to database
            room = await self.get_room(room_id)
            if room and await self.is_participant(user, room):
                message_obj = await self.create_message(user, room, message)
                
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': {
                            'id': message_obj.id,
                            'content': message_obj.content,
                            'timestamp': str(message_obj.timestamp),
                            'sender_id': user.id,
                            'sender_email': user.email,
                            'sender_profile_pic': user.profile_picture_url,
                            'room_id': room_id
                        }
                    }
                )

    async def chat_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def get_room(self, room_id):
        try:
            return ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def is_participant(self, user, room):
        return user in room.participants.all()

    @database_sync_to_async
    def create_message(self, user, room, content):
        return Message.objects.create(
            room=room,
            sender=user,
            content=content
        )

    @database_sync_to_async
    def update_user_status(self, user, status):
        user.online_status = status
        user.save()