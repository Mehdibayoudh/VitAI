from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mood
from .forms import MoodForm

@login_required
def mood_create(request):
    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user  # Assign the current user
            mood.save()
            return redirect('mood_list')
    else:
        form = MoodForm()
    return render(request, 'MentalApp/mood_form.html', {'form': form, 'action': 'Create'})

# Read (list) all moods
def mood_list(request):
    moods = Mood.objects.filter(user=request.user)
    return render(request, 'MentalApp/mood_list.html', {'moods': moods})

# Update an existing mood
def mood_update(request, mood_id):
    mood = get_object_or_404(Mood, id=mood_id, user=request.user)
    if request.method == 'POST':
        form = MoodForm(request.POST, instance=mood)
        if form.is_valid():
            form.save()
            return redirect('mood_list')
    else:
        form = MoodForm(instance=mood)
    return render(request, 'MentalApp/mood_form.html', {'form': form, 'action': 'Update'})

# Delete a mood (directly)
def mood_delete(request, mood_id):
    mood = get_object_or_404(Mood, id=mood_id, user=request.user)
    mood.delete()
    return redirect('mood_list')  # Redirect to the mood list

# Generate advice based on mood
def generate_advice(request):
    if request.method == 'POST':
        mood_id = request.POST.get('mood_id')
        mood = get_object_or_404(Mood, id=mood_id, user=request.user)
        advice = generate_advice_based_on_mood(mood.mood_description, mood.stress_level, mood.energy_level)
        return render(request, 'MentalApp/advice_output.html', {'mood': mood, 'advice': advice})
    
    # If GET, show form to select mood
    moods = Mood.objects.filter(user=request.user)
    return render(request, 'MentalApp/advice_form.html', {'moods': moods})

def generate_advice_based_on_mood(mood_description, stress_level, energy_level):
    # Advice logic based on mood description, stress level, and energy level
    if stress_level > 7:
        return "Consider taking a break and practicing relaxation techniques."
    elif energy_level < 4:
        return "Engage in light physical activity to boost your energy."
    elif mood_description.lower() == "happy":
        return "Keep enjoying the moment and share your happiness!"
    elif mood_description.lower() == "sad":
        return "It's okay to feel sad. Talk to someone you trust."
    else:
        return "Focus on self-care and try to find joy in small things."
