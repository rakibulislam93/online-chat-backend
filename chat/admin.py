from django.contrib import admin
from . import models
# Register your models here.


class ChatroomModelAdmin(admin.ModelAdmin):
    list_display = ['id','user1','user2']


admin.site.register(models.Chatroom,ChatroomModelAdmin)
admin.site.register(models.Message)