import datetime
from django.shortcuts import  render, redirect
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

def update_meal(request, idMeal):
    meal = Meal.objects.get(id=idMeal)

    if request.method == 'POST':
        meal_type = request.POST.get('meal_type')
        calories = float(request.POST.get('calories',0))
        proteins = float(request.POST.get('proteins',0))
        carbs = float(request.POST.get('carbs',0))
        fats = float(request.POST.get('fats',0))

        if not (meal_type and calories and proteins and carbs and fats):
            # If any field is missing, return an error or show a message
            return render(request, 'update-meal.html', {'meal': meal, 'error': 'Please fill in all fields.'})

        # Update the meal with the new data
        meal.meal_type = meal_type
        meal.calories = calories
        meal.proteins = proteins
        meal.carbs = carbs
        meal.fats = fats
        meal.save()
        return redirect('allMeals')  # Redirect to the list of meals


def delete_meal(request, idMeal):
    if request.method == "POST":
        meal = Meal.objects.get(id=idMeal)
        meal.delete() 
        return redirect('allMeals')  # If meal doesn't exist, redirect
    return redirect('allMeals')  # If meal doesn't exist, redirect

