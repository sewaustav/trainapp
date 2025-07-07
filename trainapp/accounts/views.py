import base64
import hmac
import json
import urllib

import requests
from django.db.models.functions import datetime
from django.http import HttpResponseRedirect, HttpResponse
from dotenv import load_dotenv

from django.shortcuts import redirect, render
from django.views import View
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from rest_framework import viewsets, generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission, SAFE_METHODS
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
        session_id = request.GET.get("session_id")
        UserAuthToken.objects.create(session_id=session_id, status=False)
        google_client_id = settings.GOOGLE_CLIENT_ID
        redirect_uri = request.build_absolute_uri('/accounts/api/google-auth/callback/')
        scope = "openid email profile"

        auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={google_client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
            f"&scope={scope}"
            f"&state={session_id}"
        )
        return redirect(auth_url)

class GoogleAuthCallbackView(View):
    def get(self, request):
        code = request.GET.get("code")
        session_id = request.GET.get("state")
        auth_model = UserAuthToken.objects.get(session_id=session_id)

        client_type = request.GET.get("client_type", "web")
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
        user, _ = User.objects.get_or_create(username=email, defaults={"email": email})
        auth_model.status = True
        auth_model.user = user
        auth_model.save()

        params = {
            'access_token': auth_data['access'],
            'refresh_token': auth_data['refresh'],
            'status': 'success'
        }
        return HttpResponse(
            """Success"""
        )



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


@api_view(["GET"])
@permission_classes([AllowAny])
def check_auth_status(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return Response({"status": False, "error": "Missing session_id"}, status=400)

    try:
        name = UserAuthToken.objects.get(session_id=session_id)
        auth = JWTToken.objects.filter(user=name.user).order_by('-created_at').first()
    except UserAuthToken.DoesNotExist:
        return Response({"status": False, "error": "Invalid session_id"}, status=404)


    # Возвращаем токены и удаляем запись
    response = {
        "status": True,
        "access_token": auth.access_token,
        "refresh_token": auth.refresh_token,
    }
    name.delete()
    return Response(response)