from django.urls import path
from . import views

urlpatterns = [
    # path('online-users/',views.OnlineUsersView.as_view()),
    path('<int:user1_id>/<int:user2_id>/messages/',views.GetMessage.as_view())
]
