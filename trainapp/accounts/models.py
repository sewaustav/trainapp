from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField


class JWTToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Token for {self.user.email}"

    class Meta:
        verbose_name = "JWT Token"
        verbose_name_plural = "JWT Tokens"


class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    week_streak = models.IntegerField(null=True, default=0)

    def __str__(self):
        return f'{self.user}'


class UserGoals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    goal = models.CharField(max_length=100)
    final_day_of_goal = models.DateField()
    status = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return f'Users {self.user} goal: {self.goal} - {self.final_day_of_goal}'

class UserAuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hash_token = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name} - auth hash token'
