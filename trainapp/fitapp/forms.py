from django import forms
from django.db import models
from .models import *
from django.forms import *
from django.contrib.auth.models import User


class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = '__all__'
        exclude = ['user']
        widgets = {'name': TextInput(attrs={'class': 'input-name-workout', 'placeholder': 'Название тренировки'}),
                   'date': DateInput(attrs={'class': 'input-date-workout', 'placeholder': 'Время'}),
                   'notes': Textarea(attrs={'class': 'input-notes-workout', 'placeholder': 'Заметки к тренировке'}), }
        labels = {'name': '',
                  'date': '',
                  'notes': ''}


class WorkoutExerciseForm(ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = '__all__'
        widgets = {'workout': TextInput(attrs={'class': 'input-exercise', 'placeholder': 'Тренировка'}),
                   'exercise': TextInput(attrs={'class': 'input-exercise', 'placeholder': 'упражнение'}),
                   'sets': NumberInput(attrs={'class': 'input-sets', 'placeholder': 'подход'}),
                   'reps': NumberInput(attrs={'class': 'input-reps', 'placeholder': 'повторения'}),
                   'weight': NumberInput(attrs={'class': 'input-weight', 'placeholder': 'вес'}), }
