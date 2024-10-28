from mongoengine import *
from UserApp.models import User

class Mood(Document):
    user = ReferenceField(User)
    mood_description = StringField(max_length=200, required=True)
    stress_level = IntField(max_length=200, required=True)
    energy_level = IntField(max_length=200, required=True)
    notes = StringField(max_length=200, required=True)
    duration = StringField(max_length=200, required=True)

    def __str__(self):
        return f"{self.user} - Mood: {self.mood_description}, Stress: {self.stress_level}, Energy: {self.energy_level}"
