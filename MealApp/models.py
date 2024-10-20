# models.py
import datetime
from mongoengine import Document, StringField, FloatField, IntField, DateField, ReferenceField
from UserApp.models import User


class Meal(Document):
    MEAL_TYPES = ('breakfast', 'lunch', 'dinner', 'snack')

    user = ReferenceField(User)  # User reference from Django's auth
    name = StringField(max_length=100, required=True)
    meal_type = StringField(choices=MEAL_TYPES, required=True)
    calories = IntField(required=True, min_value=0)
    proteins = FloatField(default=0.0)
    carbs = FloatField(default=0.0)
    fats = FloatField(default=0.0)
    date = DateField(default=datetime.date.today)

    meta = {'collection': 'meals'}

    def __str__(self):
        return f"{self.name} - {self.meal_type} ({self.calories} cal)"

