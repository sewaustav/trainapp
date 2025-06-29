import base64
import hmac
import json

import requests
import hashlib
from uuid import uuid4
import os

from django.db.models.functions import datetime
from dotenv import load_dotenv

from django.shortcuts import redirect, render
from django.views import View
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .google_auth import verify_google_id_token, create_or_get_user_and_tokens
from .models import *
from .serializers import *

load_dotenv()


# accounts api
class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('id_token')
        if not token:
            return Response({'error': 'id_token is required'}, status=400)

        idinfo = verify_google_id_token(token, settings.GOOGLE_CLIENT_ID)
        if not idinfo:
            return Response({'error': 'Invalid Google token'}, status=400)

        email = idinfo.get('email')
        name = idinfo.get('name', email)

        user, created = User.objects.get_or_create(username=email, defaults={'email': email})
        if created:
            user.set_unusable_password()
            user.save()

        refresh = RefreshToken.for_user(user)

        JWTToken.objects.create(
            user=user,
            access_token=str(refresh.access_token),
            refresh_token=str(refresh),
            expires_at=timezone.now() + timedelta(hours=48)  # Время жизни access_token
        )

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })

class GoogleAuthRedirectView(View):
    def get(self, request):
        google_client_id = settings.GOOGLE_CLIENT_ID
        redirect_uri = request.build_absolute_uri('/accounts/api/google-auth/callback/')
        scope = "openid email profile"

        auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={google_client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
            f"&scope={scope}"
        )
        return redirect(auth_url)

class GoogleAuthCallbackView(View):
    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return render(request, "accounts/auth_error.html", {"error": "No code provided."})

        token_url = "https://oauth2.googleapis.com/token"
        redirect_uri = request.build_absolute_uri('/accounts/api/google-auth/callback/')

        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        token_response = requests.post(token_url, data=data)
        token_data = token_response.json()

        id_token = token_data.get("id_token")
        if not id_token:
            return render(request, "accounts/auth_error.html", {"error": "Failed to get ID token"})



        try:
            idinfo = google_id_token.verify_oauth2_token(
                id_token, google_requests.Request(), settings.GOOGLE_CLIENT_ID
            )
        except ValueError as e:
            return render(request, "accounts/auth_error.html", {"error": str(e)})

        email = idinfo.get('email')
        name = idinfo.get('name')

        auth_data = create_or_get_user_and_tokens(
            email=idinfo.get('email'),
            name=idinfo.get('name')
        )

        payload = {
            'data': idinfo.get('name'),
            'exp': timezone.now() + timedelta(minutes=15),
            'jti': str(uuid4())
        }

        TEMP_TOKEN_SECRET = os.getenv('SECRET_AUTH_KEY')

        payload_json = json.dumps(payload, separators=(',', ':')).encode('utf-8')
        payload_b64 = base64.urlsafe_b64encode(payload_json).decode('utf-8').rstrip('=')

        signature = hmac.new(
            TEMP_TOKEN_SECRET.encode('utf-8'),
            payload_b64.encode('utf-8'),
            hashlib.sha256
        ).digest()
        signature_b64 = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip('=')

        TOKEN  = f'{payload_b64}.{signature_b64}'

        # UserAuthToken.objects.create(user=idinfo.get('name'), hash_token=TOKEN)
        # добавить deep link
        # return redirect(f'https://yourfrontend.com/#/auth-callback?token={TOKEN}')

        # frontend_redirect = f"{settings.FLUTTER_WEB_REDIRECT_URL}?access={str(auth_data['access'])}&refresh={str(auth_data['refresh'])}"
        # return redirect(frontend_redirect)



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = SaveTokenSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = RefreshTokenSerializer


class ViewProfileSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ViewProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)


class UserInfoSet(viewsets.ModelViewSet):
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserGoalsSet(viewsets.ModelViewSet):
    serializer_class = UserGoalsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserGoals.objects.filter(user=self.request.user, status=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

