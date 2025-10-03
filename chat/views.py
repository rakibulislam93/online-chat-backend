from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from . import models
from accounts.models import CustomUser

from rest_framework.permissions import IsAuthenticated
from .consumers import r,ONLINE_USERS_KEY
# Create your views here.



# class OnlineUsersView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self,request):
#         online_ids = r.smembers(ONLINE_USERS_KEY)
#         online_ids = [int(uid) for uid in online_ids if int(uid)!=request.user.id]
#         return Response({'online_users':online_ids})

class GetMessage(APIView):
    def get(self,request,user1_id,user2_id):
        print(user1_id,user2_id)
        room = models.Chatroom.objects.filter(
            user1__id__in = [user1_id,user2_id],
            user2__id__in = [user1_id,user2_id]
        ).first()
        print(room)
        if room:
            messages = models.Message.objects.filter(room=room)
            serializer = serializers.MessageSerializer(messages,many=True)
            return Response(serializer.data,status=200)
        
        return Response({"messages":[]},status=200)
        
