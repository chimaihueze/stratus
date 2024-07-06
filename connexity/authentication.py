from rest_framework_simplejwt.tokens import RefreshToken


def refresh_token(user):
    """
    create refresh token
    """
    return RefreshToken.for_user(user)

