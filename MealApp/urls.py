from django.urls import path
from . import views

urlpatterns = [

    path('allMeals', views.meal_list, name='allMeals'),
    path('addMeal', views.add_meal, name='addMeal'),

]
