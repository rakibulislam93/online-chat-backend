from django.db import models
from accounts.models import CustomUser
# Create your models here.


class Chatroom(models.Model):
    user1 = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='chat_user1')
    user2 = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='chat_user2')
    created_at = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user1','user2')

    def save(self,*args, **kwargs):
        if self.user1.id > self.user2.id:
            self.user1,self.user2 = self.user2,self.user1
        
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.user1.username} --- {self.user2.username}"
    
class Message(models.Model):
    room = models.ForeignKey(Chatroom,on_delete=models.CASCADE,related_name='messages')
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='sent_messages')
    content = models.TextField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.sender.username} ---->{self.content} "