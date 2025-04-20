from django.shortcuts import render, redirect

from .forms import WorkoutForm, WorkoutExerciseForm
from .models import *
from django.views.generic import *

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import *


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

def WorkoutFunc(request, program_name):
    form = WorkoutForm()
    program = Dprogram.objects.get(name=program_name)
    exercises = ProgramExercise.objects.filter(program=program)
    if request.method == 'POST':
        workout = WorkoutResult.objects.create(
            user=request.user,
            name=request.POST.get('name', 'Без названия'),
            notes=request.POST.get('notes', '')
        )
        for ex_index, program_ex in enumerate(exercises):
            sets = program_ex.sets
            exercise = program_ex.exercise

            for set_index in range(sets):
                weight_key = f"form-{ex_index}-{set_index}-weight"
                reps_key = f"form-{ex_index}-{set_index}-reps"
                weight = request.POST.get(weight_key)
                reps = request.POST.get(reps_key)

                if weight and reps:
                    WorkoutResultSet.objects.create(
                        workout=workout,
                        exercise=exercise,
                        set=set_index + 1,
                        weight=float(weight),
                        rep=int(reps)
                    )

        return redirect('mainpage')


    data = {
        'form':form,
        'exercise': exercises,
    }

    return render(request, 'fitapp/training-single.html', data)

class ProgramList(ListView):
    model = Dprogram
    context_object_name = 'programs'
    template_name = 'fitapp/program-list.html'

def DetailProgram(request, program_name):
    program = Dprogram.objects.get(name=program_name)
    exercises = ProgramExercise.objects.filter(program=program)

    data = {
        'title': program_name,
        'exercises': exercises,
    }

    return render(request, 'fitapp/program-detail.html', data)


# api
class FitapplistViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

class WorkoutlistViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

class WorkoutExerciselistViewSet(viewsets.ModelViewSet):
    queryset = WorkoutExercise.objects.all()
    serializer_class = WorkoutExerciseSerializer
    permission_classes = [IsAuthenticated]

class DprogramlistViewSet(viewsets.ModelViewSet):
    queryset = Dprogram.objects.all()
    serializer_class = DprogramSerializer
    permission_classes = [IsAuthenticated]


class ProgramExerciselistViewSet(viewsets.ModelViewSet):
    queryset = ProgramExercise.objects.all()
    serializer_class = ProgramExerciseSerializer
    permission_classes = [IsAuthenticated]


class WorkoutResultlistViewSet(viewsets.ModelViewSet):
    queryset = WorkoutResult.objects.all()
    serializer_class = WorkoutResultSerializer
    permission_classes = [IsAuthenticated]


class WorkoutResultSetlistViewSet(viewsets.ModelViewSet):
    queryset = WorkoutResultSet.objects.all()
    serializer_class = WorkoutResultSetSerializer
    permission_classes = [IsAuthenticated]

