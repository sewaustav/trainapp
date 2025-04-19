from django.shortcuts import render, redirect

from trainapp.fitapp.forms import WorkoutForm, WorkoutExerciseForm


def mainpage(request):
    # здесь другие разрабы будут вставлять код
    # Рома если ты каким-то чудом зашел сюда, знай, что...
    # Чтобы узнать продолжение, приобретите подписку уровня pro
    return render(request, 'fitapp/main.html')


def constructor(request):
    if request.method == "POST":
        if 'workout-btn' in request.POST:
            form = WorkoutForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('mainpage')
        elif 'workout-exercise-btn' in request.POST:
            form_workout = WorkoutExerciseForm(request.POST)
            if form_workout.is_valid():
                form_workout.save()
                return redirect('mainpage')
    data = {'form': WorkoutForm(), 'workout-exercise-form': WorkoutExerciseForm()}

    return render(request, 'fitapp/constructor.html', data)
