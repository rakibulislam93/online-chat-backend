from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.RegisterApiView.as_view(),name='register'),
    path('activate/<uidb64>/<token>/',views.AccountActivateView.as_view()),
    path('login/',views.LoginView.as_view(),name='login'),
    path('password/change/',views.PasswordChangeView.as_view()),
    path('reset/password/',views.PasswordResetView.as_view()),
    path('reset/password/<uidb64>/<token>/',views.SetNewPasswordView.as_view()),
    path('users/',views.AllUserListView.as_view(),name='all_users'),
]
