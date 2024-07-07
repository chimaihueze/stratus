from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.authentication import refresh_token
from users.models import User
from users.serializers import RegisterUserSerializer, UserSerializer


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
                        "userId": user.userId,
                        "firstName": user.firstName,
                        "lastName": user.lastName,
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
        }
        return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user:
            token = refresh_token(user).access_token
            response = {
                "status": "success",
                "message": "Login successful",
                "data": {
                    "accessToken": str(token),
                    "user": {
                        "userId": user.userId,
                        "firstName": user.firstName,
                        "lastName": user.lastName,
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


class UserView(APIView):
    serializer_class = UserSerializer

    def get(self, request, pk):
        user = request.user

        try:
            user_record = User.objects.get(pk=pk)

            if user == user_record or user_record.organisations.filter(users=user).exists():
                response = {
                    "status": "success",
                    "message": "User record retrieved successfully",
                    "data": {
                        "userId": user.userId,
                        "firstName": user.firstName,
                        "lastName": user.lastName,
                        "email": user.email,
                        "phone": user.phone
                    }
                }
                return Response(response, status.HTTP_200_OK)

            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
