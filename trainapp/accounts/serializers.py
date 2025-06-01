from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'

class UserGoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGoals
        fields = '__all__'

class SaveTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        JWTToken.objects.create(
            user=self.user,
            access_token=data['access'],
            refresh_token=data['refresh'],
            expires_at=timezone.now() + timedelta(hours=24 * 7)
        )
        return data

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class ViewProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'