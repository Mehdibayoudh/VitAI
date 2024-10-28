from django.urls import path
from . import views

urlpatterns = [
    path('mood/input/', views.mood_create, name='mood_create'),
    path('mood/list/', views.mood_list, name='mood_list'),
    path('mood/update/<str:mood_id>/', views.mood_update, name='mood_update'),
    path('mood/delete/<str:mood_id>/', views.mood_delete, name='mood_delete'),
    path('mood/show/<str:mood_id>/', views.mood_show, name='mood_show'),
    path('mood/advice/<str:mood_id>/', views.advice_generator, name='advice_generator'), 
]
