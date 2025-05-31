from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework_simplejwt.tokens import RefreshToken

from .models import JWTToken


def verify_google_id_token(token, valid_client_id):
    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), audience=valid_client_id)
        return idinfo
    except ValueError:
        return None


def create_or_get_user_and_tokens(email, name=None):
    user, created = User.objects.get_or_create(
        username=email,
        defaults={"email": email}
    )

    if created:
        user.set_unusable_password()
        user.save()

    refresh = RefreshToken.for_user(user)

    JWTToken.objects.create(
        user=user,
        access_token=str(refresh.access_token),
        refresh_token=str(refresh),
        expires_at=timezone.now() + timedelta(hours=24*7)
    )

    return {
        'user': user,
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

