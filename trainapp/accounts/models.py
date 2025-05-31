from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField


class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    week_streak = models.IntegerField(null=True, default=0)

    def __str__(self):
        return f'{self.user}'


class UserGoals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = CharField(max_length=100)
    final_day_of_goal = models.DateField()

    def __str__(self):
        return f'Users {self.user} goal: {self.goal} - {self.final_day_of_goal}'
