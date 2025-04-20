from django.shortcuts import render, redirect

from .forms import WorkoutForm, WorkoutExerciseForm
from .models import *


def mainpage(request):
    # здесь другие разрабы будут вставлять код
    # Рома если ты каким-то чудом зашел сюда, знай, что...
    # Чтобы узнать продолжение, приобретите подписку уровня pro
    return render(request, 'fitapp/main.html')


def constructor(request):
    if request.method == "POST":
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            total_forms = int(request.POST.get("form-TOTAL_FORMS", 0))
            for i in range(total_forms):
                exercise_id = request.POST.get(f"form-{i}-exercise")
                sets = request.POST.get(f"form-{i}-sets")
                reps = request.POST.get(f"form-{i}-reps")
                weight = request.POST.get(f"form-{i}-weight")
                if exercise_id and sets and reps and weight:
                    exercise = Exercise.objects.get(id=exercise_id)
                    WorkoutExercise.objects.create(
                        workout=workout,
                        exercise=exercise,
                        sets=sets,
                        reps=reps,
                        weight=weight,
                    )
            return redirect('mainpage')
    else:
            workout_form = WorkoutForm()
    data = {'form': WorkoutForm(),
            'workout-exercise-form': WorkoutExerciseForm(),
            'exercises': Exercise.objects.all()
            }

    return render(request, 'fitapp/constructor.html', data)
