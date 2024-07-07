from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from organisation.models import Organisation
from organisation.serializers import OrganisationSerializer
from users.models import User


class OrganisationView(APIView):

    def get(self, request):
        user = request.user
        organisations = user.organisations.all()

        serializer = OrganisationSerializer(organisations, many=True)

        response = {
            "status": "success",
            "message": "List Of Organisations",
            "data": {
                "organisations": serializer.data
            }
        }
        return Response(response, status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
            response = {
                "status": "success",
                "message": "Organisation created successfully",
                "data": {
                    "orgId": organisation.orgId,
                    "name": organisation.name,
                    "description": organisation.description
                }
            }
            return Response(response, status.HTTP_201_CREATED)
        response = {
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
        }
        return Response(response, status.HTTP_400_BAD_REQUEST)


class GetOrganisationView(APIView):
    def get(self, request, pk):
        organisation = Organisation.objects.get(pk=pk)
        serializer = OrganisationSerializer(organisation)

        if organisation:
            response = {
                "status": "success",
                "message": "<message>",
                "data": serializer.data
            }
            return Response(response, status.HTTP_200_OK)
        response = {
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
        }
        return Response(response, status.HTTP_400_BAD_REQUEST)


class CreateOrganisationView(APIView):
    def post(self, request):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
            user = request.user
            organisation.users.add(user)
            response = {
                "status": "success",
                "message": "Organisation created successfully",
                "data": {
                    "orgId": organisation.orgId,
                    "name": organisation.name,
                    "description": organisation.description
                }
            }
            return Response(response, status.HTTP_201_CREATED)
        response = {
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
        }
        return Response(response, status.HTTP_400_BAD_REQUEST)


class AddUserToOrganisationView(APIView):
    def post(self, request, pk):
        user = User.objects.get(pk=request.data)
        organisation = Organisation.objects.get(orgId=pk)

        if user and organisation:
            organisation.users.add(user)
            organisation.save()

            response = {
                "status": "success",
                "message": "User added to organisation successfully"
            }
            return Response(response, status=status.HTTP_200_OK)
