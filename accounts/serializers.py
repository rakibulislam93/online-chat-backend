from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from . import models
User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','username','email','password','confirm_password']
        
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        email = attrs.get('email')
        password1 = attrs.get('password')
        password2 = attrs.get('confirm_password')
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error':'Email already exists!'})
        
        validate_password(password1)
        
        if password1 != password2:
            raise serializers.ValidationError({'error':'password not match!'})
        
        return attrs
    
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active=False
        user.save()
        
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        password1 = attrs.get('new_password')
        password2 = attrs.get('confirm_password')
        validate_password(password1)
        if password1 != password2:
            raise serializers.ValidationError({'error':'password do not match.!'})
        
        return attrs
    


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True,validators=[validate_password])
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','is_online','last_active']
    
    
