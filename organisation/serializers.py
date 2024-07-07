from rest_framework import serializers

from organisation.models import Organisation


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['orgId', 'name', 'description']

    def create(self, validated_data):
        organisation = Organisation.objects.create(**validated_data)
        return organisation
