import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from accounts.models import CustomUser
from . import models
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            print('****************')
            await self.set_user_online(self.user)
        print(self.user.username)
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.room = await self.get_or_create_room(self.user.id,self.receiver_id)
        self.room_group_name = f'chat_{self.room.id}'
        
        print(self.receiver_id)
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        
        await self.accept()
    
    
    async def disconnect(self, code):
        if self.user.is_authenticated:
            await self.set_user_offline(self.user)
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)

    async def receive(self, text_data = None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        new_msg = await self.save_messages(self.user.id,self.room.id,message)
        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chat.message',
                "message": new_msg["content"],
                "sender": new_msg["sender"],
            }
        )

    async def chat_message(self,event):
        message = event['message']
        sender = event['sender']
        await self.send(text_data=json.dumps({"message":message,"sender":sender}))
    
    
    @database_sync_to_async
    def get_or_create_room(self,user1_id,user2_id):
        user1_id = int(user1_id)
        user2_id = int(user2_id)
        first_id, second_id = sorted([user1_id, user2_id])
        user1 = CustomUser.objects.get(id=first_id)
        user2 = CustomUser.objects.get(id=second_id)
        room,_ = models.Chatroom.objects.get_or_create(
            user1 = user1,
            user2 = user2
        )
        print(room)
        return room

    @database_sync_to_async
    def save_messages(self,sender_id,room_id,content):
        sender = CustomUser.objects.get(id=sender_id)
        room = models.Chatroom.objects.get(id=room_id)
        msg = models.Message.objects.create(sender=sender,room=room,content=content)
        
        return{
            "id":msg.id,
            "sender":sender.username,
            "content":msg.content
        }
        
    @database_sync_to_async
    def set_user_online(self, user):
        user.is_online = True
        user.save(update_fields=["is_online", "last_active"])

    @database_sync_to_async
    def set_user_offline(self, user):
        user.is_online = False
        user.last_active = timezone.now()
        user.save(update_fields=["is_online", "last_active"])