from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from connexity.authentication import refresh_token
from connexity.serializers import RegisterUserSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = RegisterUserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            token = refresh_token(user).access_token
            response = {
                "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": str(token),
                    "user": {
                        "userId": user.pk,
                        "firstName": user.first_name,
                        "lastName": user.last_name,
                        "email": user.email,
                        "phone": user.phone
                    }
                }
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 400,
            "errors": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user:
            token = refresh_token(user)
            response = {
                "status": "success",
                "message": "Login successful",
                "data": {
                    "accessToken": str(token),
                    "user": {
                        "userId": user.pk,
                        "firstName": user.first_name,
                        "lastName": user.last_name,
                        "email": user.email,
                        "phone": user.phone,
                    }
                }
            }
            login(request, user)
            return Response(response, status.HTTP_200_OK)
        else:
            response = {
                "status": "Bad request",
                "message": "Authentication failed",
                "statusCode": 401
            }
            return Response(response, status.HTTP_401_UNAUTHORIZED)
