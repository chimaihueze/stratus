import uuid

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
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
        user = request.user

        try:
            organisation = Organisation.objects.get(pk=pk)
            serializer = OrganisationSerializer(organisation)

            if organisation in user.organisations.all():
                response = {
                    "status": "success",
                    "message": "Organisation details retrieved successfully",
                    "data": serializer.data
                }
                return Response(response, status.HTTP_200_OK)
            response = {
                "status": "Bad Request",
                "message": "Client error",
                "statusCode": 400
            }
            return Response(response, status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({"error": "Organisation does not exist"})


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
        try:
            user_id = request.data.get('userId')
            user_id = uuid.UUID(user_id)

            user = get_object_or_404(User, userId=user_id)
            organisation = get_object_or_404(Organisation, orgId=pk)

            if user and organisation:
                user.organisations.add(organisation)
                user.save()

                response = {
                    "status": "success",
                    "message": "User added to organisation successfully"
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                raise ValidationError("Invalid user or organisation")

        except (ValueError, ValidationError) as e:
            response = {
                "status": "Bad Request",
                "message": str(e),
                "statusCode": 400
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
