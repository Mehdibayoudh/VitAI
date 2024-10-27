from django import forms

class MoodInputForm(forms.Form):
    mood = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'How do you feel?'}))
