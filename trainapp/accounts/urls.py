from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

router = DefaultRouter()
router.register(r'profile', ViewProfileSet, basename='profile')
router.register(r'user-goals', UserGoalsSet, basename='goals')
router.register(r'user-info', UserInfoSet, basename='exta-info')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('api/google-login/', GoogleLoginView.as_view(), name='google-login'),
    path("api/google-auth/", GoogleAuthRedirectView.as_view(), name="google-auth-start"),
    path("api/google-auth/callback/", GoogleAuthCallbackView.as_view(), name="google-auth-callback"),
]
