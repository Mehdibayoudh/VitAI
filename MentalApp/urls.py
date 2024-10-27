from django.urls import path
from . import views

urlpatterns = [
    path('mood/input/', views.mood_create, name='mood_create'),
    path('mood/list/', views.mood_list, name='mood_list'),
    path('mood/update/<int:mood_id>/', views.mood_update, name='mood_update'),
    path('mood/delete/<int:mood_id>/', views.mood_delete, name='mood_delete'),
    path('mood/advice/', views.generate_advice, name='generate_advice'), 
]
