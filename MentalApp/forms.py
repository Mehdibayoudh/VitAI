from django import forms
from .models import Mood

class MoodForm(forms.ModelForm):
    class Meta:
        model = Mood
        fields = ['mood_description', 'stress_level', 'energy_level', 'notes', 'duration']
