from django.urls import path
from . import views

urlpatterns = [

    path('allMeals', views.meal_list, name='allMeals'),
    path('addMeal', views.add_meal, name='addMeal'),
    path('delete/<str:idMeal>/', views.delete_meal, name='delete_meal'),  
    path('update/<str:idMeal>/', views.update_meal, name='update_meal'),  

]
