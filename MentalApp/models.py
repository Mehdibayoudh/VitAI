from django.db import models
from django.contrib.auth.models import User

class Mood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the user
    mood_description = models.CharField(max_length=255)  # Mood as a string
    stress_level = models.IntegerField(default=0)  # Stress level (0-10 scale)
    energy_level = models.IntegerField(default=5)  # Energy level (0-10 scale)
    notes = models.TextField(blank=True, null=True)  # Additional notes (optional)
    duration = models.CharField(max_length=100, blank=True, null=True)  # Duration of mood state (e.g., "1 hour", "all day")

    def __str__(self):
        return f"{self.user.username} - Mood: {self.mood_description}, Stress: {self.stress_level}, Energy: {self.energy_level}"
