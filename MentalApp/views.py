from django.shortcuts import render
from .forms import MoodInputForm

def mood_input(request):
    recommendations = None
    if request.method == 'POST':
        form = MoodInputForm(request.POST)
        if form.is_valid():
            mood = form.cleaned_data['mood']
            # Here you'll eventually fetch recommendations based on the mood
    else:
        form = MoodInputForm()

    return render(request, 'mood_app/mood_input.html', {'form': form, 'recommendations': recommendations})
