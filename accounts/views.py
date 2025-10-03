from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from . import serializers
from . import models

from chat.consumers import r,ONLINE_USERS_KEY
# Create your views here.


class RegisterApiView(CreateAPIView):
    serializer_class = serializers.RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        confirm_link = f'http://127.0.0.1:8000/accounts/activate/{uid}/{token}/'
        subject = 'Account activation'
        send_mail(
            subject=subject,
            message= f'Please click the link and activate your account {confirm_link}',
            from_email='example.com',
            recipient_list=[user.email],
            fail_silently=False
        )
        return Response({'message':'please check your mail and activate your account..'},status=201)



class AccountActivateView(APIView):
    def get(self,request,*args, **kwargs):
        uid = urlsafe_base64_decode(kwargs['uidb64']).decode()
        token = kwargs['token']
        
        try:
            user = models.CustomUser.objects.get(pk=uid)
        except(TypeError,ValueError,OverflowError,models.CustomUser.DoesNotExist):
            return Response({'error':'Invalid user'},status=400)
        
        if not default_token_generator.check_token(user,token):
            return Response({'error':'Invalid user or expired token'},status=400)
        
        user.is_active=True
        user.save()
        return Response({'message':'Account activate successful.'},status=200)


class LoginView(APIView):
    serializer_class = serializers.LoginSerializer
    def post(self,request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username,password=password)
        if not user:
            return Response({'error':'Invalid credentails.!'},status=400)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh':str(refresh),
            'access':str(refresh.access_token),
            'message':'Login successful',
            'username':user.username,
            'user_id':user.id
        })
        


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PasswordChangeSerializer
    def put(self,request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        old_password = serializer.data['old_password']
        new_password = serializer.validated_data['new_password']
        if not user.check_password(old_password):
            return Response({'error':'Old password is incorrect!'})
        
        user.set_password(new_password)
        user.save()
        return Response({
            'message':'password change successful'
        },status=200)
        

class PasswordResetView(APIView):
    serializer_class = serializers.PasswordResetSerializer
    def post(self,request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        if not models.CustomUser.objects.filter(email=email).exists():
            return Response({'error':'No user found with this email'},status=400)
        
        user = models.CustomUser.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        reset_link = f'http://127.0.0.1:8000/accounts/reset/password/{uid}/{token}/'
        
        send_mail(
            subject='Reset Your password',
            from_email='example.com',
            recipient_list=[email],
            message=f'please click the link and set your new password {reset_link}',
            fail_silently=False
        )
        return Response({'message':'Please check your main and set your new password'},status=200)


class SetNewPasswordView(APIView):
    serializer_class = serializers.SetNewPasswordSerializer
    def post(self,request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']
        try:
            uid = urlsafe_base64_decode(kwargs['uidb64']).decode()
            user = models.CustomUser.objects.get(pk=uid)
        except(TypeError,ValueError,OverflowError,models.CustomUser.DoesNotExist):
            return Response({'error':'Invalid user'},status=400)
        
        if not default_token_generator.check_token(user,kwargs['token']):
            return Response({'error':'Invalid user or expired token'},status=400)
        user.set_password(new_password)
        user.save()
        return Response({'message':'Your password reset successful..'},status=200)



class AllUserListView(APIView):
    def get(self,request,format=None):
        users = models.CustomUser.objects.values("id","username")
        online_ids = r.smembers(ONLINE_USERS_KEY)
        online_ids = [ int(uid) for uid in online_ids]
        user_list = []
        for user in users:
            user_list.append({
                "id":user["id"],
                "username":user["username"],
                "is_online":user['id'] in online_ids
            })
        return Response(user_list,status=200)
        
