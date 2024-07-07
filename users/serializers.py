from rest_framework import serializers

from organisation.services import create_organisation
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']


class RegisterUserSerializer(UserSerializer):
    password = serializers.CharField(write_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        create_organisation(user)
        return user


class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField()
