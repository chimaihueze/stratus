from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from users.views import LoginView, RegisterView

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token-refresh-pair'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
]
