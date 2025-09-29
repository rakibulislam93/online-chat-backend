from django.contrib import admin
from . import models
# Register your models here.

class CustomUserModelAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','is_active']
admin.site.register(models.CustomUser,CustomUserModelAdmin)
