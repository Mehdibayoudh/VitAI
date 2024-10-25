import datetime
from django.shortcuts import  render, redirect
from .models import Meal
from UserApp.models import User

from django.http import JsonResponse

import google.generativeai as genai

genai.configure(api_key="AIzaSyD6PHqbtnPOl22yrLDcPA4vEQ0YrBhih0s")
# genai.configure(api_key=os.environ["API_KEY"])



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



def calorie_calculator(request):
    if request.method == 'POST':
        age = request.POST.get('age')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        activity = request.POST.get('activity')

        # Gemini API prompt
        prompt = (
            f"I am {age} years old, my height is {height} cm, and I weigh {weight} kg. "
            f"My activity level is: {activity}. How many calories should I consume "
            f"to maintain, gain muscle, or cut?"
            f"just be straight to the point and give estamitions"
            f"and put each info in a line , make it look professional"
        )

        try:
            # Call Gemini API
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            calories_response = response.text
            # Assume calories_response is the string you get from the API.
            calories_response = response.text.strip().split('\n')
            calories_output = "<br>".join(calories_response)  # Join lines with HTML line breaks


            # Return a JSON response to be handled by JavaScript
             # Render the all-meals.html with the calories included in the context
            return render(request, 'all-meals.html', {'calories': calories_output})

        except Exception as e:
            return render(request, 'all-meals.html', {'error': str(e)})
        
    # Render form if GET request
    return render(request, 'all-meals.html')