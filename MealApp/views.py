import datetime
from django.shortcuts import render, redirect
from .models import Meal
from UserApp.models import User

from django.http import HttpResponse


def meal_list(request):
    # meals = Meal.objects(user=request.user, date=datetime.date.today())
    meals = Meal.objects(user=User.objects.get(id="67152708d4517e74c43080b3"), date=datetime.date.today()) #hard coding the user for now
    total_calories = sum(meal.calories for meal in meals)
    return render(request, 'all-meals.html', {'meals': meals, 'total_calories': total_calories})


def add_meal(request):
    if request.method == 'POST':
        meal = Meal(
            # user=request.user,
            user=User.objects.get(id="67152708d4517e74c43080b3"),  #hard coding the user for now
            name=request.POST['name'],
            meal_type=request.POST['meal_type'],
            calories=request.POST['calories'],
            proteins=request.POST.get('proteins', 0.0),
            carbs=request.POST.get('carbs', 0.0),
            fats=request.POST.get('fats', 0.0)
        )
        meal.save()
        return redirect('allMeals')
    return render(request, 'add-meal.html')

