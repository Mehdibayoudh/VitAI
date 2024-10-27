from django.urls import path
from .views import mood_input

urlpatterns = [
    path('', mood_input, name='mood_input'),
]
