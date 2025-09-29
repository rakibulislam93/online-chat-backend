from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    is_online = models.BooleanField(default=False)
    last_active = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self):
        return self.username



    