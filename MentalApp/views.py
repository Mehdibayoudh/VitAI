from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mood
from UserApp.context_processors import user_context
import google.generativeai as genai

genai.configure(api_key="AIzaSyD6PHqbtnPOl22yrLDcPA4vEQ0YrBhih0s")

def mood_create(request):
    if request.method == 'POST':
        context = user_context(request)
        userC = context['user']
        
        user = userC
        mood_description = request.POST.get('mood_description')
        stress_level = int(request.POST.get('stress_level'))
        energy_level = int(request.POST.get('energy_level'))
        notes = request.POST.get('notes')
        duration = request.POST.get('duration')
        
        # Create and save the Mood instance
        mood = Mood(
            user=user,  # Automatically assign the logged-in user
            mood_description=mood_description,
            stress_level=stress_level,
            energy_level=energy_level,
            notes=notes,
            duration=duration
        )
        mood.save()
        
        return redirect('mood_list')  # Redirect to mood list after submission

    return render(request, 'mentalApp/add_mood.html')

# Read (list) all moods
def mood_list(request):
    context = user_context(request)
    user = context['user']
    
    moods = Mood.objects(user = user)
    return render(request, 'MentalApp/mood_list.html', {'moods': moods})

# Update an existing mood
def mood_update(request, mood_id):
    mood = Mood.objects.get(id=mood_id)

    if request.method == 'POST':
        mood_description = request.POST.get('mood_description')
        stress_level = int(request.POST.get('stress_level'))
        energy_level = int(request.POST.get('energy_level'))
        notes = request.POST.get('notes')
        duration = request.POST.get('duration')

        if not (mood_description and stress_level and energy_level ):
            # If any field is missing, return an error or show a message
            return render(request, 'update-meal.html', {'meal': meal, 'error': 'Please fill in all fields.'})

        # Update the meal with the new data
        mood.mood_description = mood_description
        mood.stress_level = stress_level
        mood.energy_level = energy_level
        mood.notes = notes
        mood.duration = duration
        mood.save()
        return redirect('mood_list')  # Redirect to the list of meals
    return render(request, 'MentalApp/update_mood.html', {'mood': mood})

# Delete a mood (directly)
def mood_delete(request, mood_id):
    mood = Mood.objects.get(id=mood_id)
    mood.delete()
    return redirect('mood_list')  # Redirect to the mood list

def mood_show(request, mood_id):
    mood = Mood.objects.get(id=mood_id)
    return render(request, 'MentalApp/show_mood.html', { 'mood': mood, 'advices': "" })


def advice_generator(request, mood_id):

    mood = Mood.objects.get(id=mood_id)

    prompt = (
        f"I feel {mood.mood_description}, my stress level is {mood.stress_level}. "
        f"my energy level is {mood.energy_level}. Also {mood.notes} "
        f"i'm feeling this for {mood.duration} min"
        f"just be straight to the point and give mental advices on how to handle this"
        f"and put each advice in a line"
    )

    try:
        # Call Gemini API
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        advices_response = response.text
        advice_list = [item.strip() for item in advices_response.split('.') if item.strip()]

        return render(request, 'MentalApp/show_mood.html', {'mood': mood ,'advices': advice_list})

    except Exception as e:
        return render(request, 'MentalApp/show_mood.html', { 'mood': mood, 'advices': "" })
