from rest_framework import serializers
from . import models


class ChatroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chatroom
        fields = ['id','user1','user2','created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender",read_only=True)
    class Meta:
        model = models.Message
        fields = ['id','room','sender','content','is_seen','sender_name']