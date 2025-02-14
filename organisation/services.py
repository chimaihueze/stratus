from organisation.models import Organisation


def create_organisation(user):
    """
    method to create organisation
    """
    organisation_name = f"{user.firstName.title()}'s Organisation"
    organisation = Organisation.objects.create(name=organisation_name)

    return user.organisations.add(organisation)
