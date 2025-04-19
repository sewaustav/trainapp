from django import forms
from django.db import models
from .models import *
from django.forms import *
from django.contrib.auth.models import User


class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = '__all__'
        widgets = {'user': TextInput(attrs={'class': 'input-name-workout', 'placeholder': 'Название тренировки'}),
                   'date': DateInput(attrs={'class': 'input-date-workout', 'placeholder': 'МЫ пока не знаем че делает эта хуйня(введите время)'}),
                   'notes': Textarea(attrs={'class': 'input-notes-workout', 'placeholder': 'Введите <UNK> <UNK> <UNK> <UNK> <UNK> <UNK>(<UNK> <UNK>)'}), }
        labels = {'user': '',
                  'date': '',
                  'notes': ''}


class WorkoutExerciseForm(ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = '__all__'
        widgets = {'workout': TextInput(attrs={'class': 'input-exercise', 'placeholder': '<UNK> <UNK>'}),
                   'exercise': TextInput(attrs={'class': 'input-exercise', 'placeholder': '<UNK> <UNK> <UNK> <UNK>'}),
                   'sets': IntegerField(attrs={'class': 'input-sets', 'placeholder': '<UNK> <UNK> <UNK> <UNK> <UNK>'}),
                   'reps': IntegerField(attrs={'class': 'input-reps', 'placeholder': '<UNK> <UNK> <UNK> <UNK> <UNK>'}),
                   'weight': FloatField(attrs={'class': 'input-weight', 'placeholder': '<UNK> <UNK> <UNK> <UNK> <UNK>'}), }
