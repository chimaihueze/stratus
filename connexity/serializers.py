from rest_framework import serializers

from connexity.models import User
from organisation.models import Organisation


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

        organisation_name = f"{user.first_name.title()}'s Organisation"
        organisation = Organisation.objects.create(name=organisation_name)

        user.organisations.add(organisation)
        return user



