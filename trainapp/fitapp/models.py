from django.db import models
from datetime import *
from django.contrib.auth.models import User

# при изменении дефолтной модели User обязательно добавить поля : рост - float; вес - float; жим, становая, присед, бицепс - float

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    muscle_group = models.CharField(max_length=100)
    rating = models.IntegerField(blank=True, null=True)
    img = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Exercise"
        verbose_name_plural = "Exercise"

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workouts")
    date = models.DateField(default=datetime.now())
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    class Meta:
        verbose_name = "Workout"
        verbose_name_plural = "Workout"

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="exercises")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.FloatField()

    def __str__(self):
        return f"{self.exercise.name} on {self.workout.date}"

    class Meta:
        verbose_name = "WorkoutExercise"
        verbose_name_plural = "WorkoutExercise"

class Dprogram(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type_of_program = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Dprogram"
        verbose_name_plural = "Dprogram"

class ProgramExercise(models.Model):
    program = models.ForeignKey(Dprogram, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.FloatField()

    def __str__(self):
        return f"{self.exercise.name} on {self.program.name}"

    class Meta:
        verbose_name = "ProgramExercise"
        verbose_name_plural = "ProgramExercise"
