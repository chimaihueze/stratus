from django.urls import path

from organisation.views import OrganisationView, GetOrganisationView, AddUserToOrganisationView, CreateOrganisationView

urlpatterns = [
    path('', OrganisationView.as_view(), name='user-organisations'),
    path('/<str:pk>', GetOrganisationView.as_view(), name='organisation'),
    path('/<str:pk>/users', AddUserToOrganisationView.as_view(), name='add-to-organisation'),
    path('', CreateOrganisationView.as_view(), name='create-organisation'),
]
