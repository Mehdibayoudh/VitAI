
from django.shortcuts import render, redirect
from .models import Exercise
from .forms import ExerciseForm

def create_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('exercise_list')
    else:
        form = ExerciseForm()
    return render(request, 'exercise_form.html', {'form': form})

def exercise_list(request):
    exercises = Exercise.objects.all()
    return render(request, 'exercise_list.html', {'exercises': exercises})

def update_exercise(request, pk):
    exercise = Exercise.objects.get(pk=pk)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect('exercise_list')
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'exercise_form.html', {'form': form})

def delete_exercise(request, pk):
    exercise = Exercise.objects.get(pk=pk)
    if request.method == 'POST':
        exercise.delete()
        return redirect('exercise_list')
    return render(request, 'exercise_confirm_delete.html', {'exercise': exercise})
