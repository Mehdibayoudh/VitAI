from django import forms
from .models import Exercise

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'category', 'muscles_targeted', 'description', 'duration', 'calories_burned_per_minute', 'image']
