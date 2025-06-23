from django.db import models
from datetime import *
from django.contrib.auth.models import User
from django.db.models import CharField
from kivy.tools.pep8checker.pep8 import blank_lines


class Exercise(models.Model):
    # add equipment
    name = models.CharField(max_length=100, unique=True)
    muscle_group = models.CharField(max_length=100)
    second_group = models.CharField(max_length=100, null=True, blank=True)
    third_group = models.CharField(max_length=100, null=True, blank=True)
    rating = models.IntegerField(blank=True, null=True)
    img = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Exercise"
        verbose_name_plural = "Exercise"


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workouts")
    name = models.CharField(max_length=100, null=True)
    date = models.DateField(default=datetime.now(), blank=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="program")
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
    weight = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.exercise.name} on {self.program.name}"

    class Meta:
        verbose_name = "ProgramExercise"
        verbose_name_plural = "ProgramExercise"

class WorkoutResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(default=datetime.now(), blank=True)
    notes = models.TextField(blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    tonnage = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.name}'

    class Meta:
        verbose_name = "WorkoutResult"
        verbose_name_plural = "WorkoutResult"

class WorkoutResultSet(models.Model):
    workout = models.ForeignKey(WorkoutResult, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    set = models.IntegerField()
    rep = models.IntegerField()
    weight = models.FloatField()

    def __str__(self):
        return f"{self.exercise.name} - {self.workout.name}"

    class Meta:
        verbose_name = "WorkoutResultSet"
        verbose_name_plural = "WorkoutResultSet"

class FutureWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(default=datetime.now(), blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.name} - {self.date}'

    class Meta:
        verbose_name = "FutureTraining"
        verbose_name_plural = "FutureTraining"

class FutureWorkoutExercise(models.Model):
    workout = models.ForeignKey(FutureWorkout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    reps = models.IntegerField()
    weight = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.exercise.name} - {self.workout.name}"

    class Meta:
        verbose_name = "FutureTrainingExercises"
        verbose_name_plural = "FutureTrainingExercises"