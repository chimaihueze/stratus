from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from users.views import LoginView, RegisterView, UserView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),

    path('api/users/<str:pk>', UserView.as_view(), name='user-detail')
]
