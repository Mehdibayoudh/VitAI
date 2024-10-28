"""vitai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from Exercise import views as ExerciseViews 
from django.urls import path, include

from UserApp import views as Userviews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', Userviews.home, name='home'),
    path('users/', include('UserApp.urls')),

    path('admin/', admin.site.urls),

     # Exercise app URLs
    path('exercises/', ExerciseViews.exercise_list, name='exercise_list'),  # List exercises
    path('exercises/create/', ExerciseViews.create_exercise, name='create_exercise'),  # Create an exercise
    path('exercises/update/<int:pk>/', ExerciseViews.update_exercise, name='update_exercise'),  # Update an exercise
    path('exercises/delete/<int:pk>/', ExerciseViews.delete_exercise, name='delete_exercise'),
    path('exercise/<int:exercise_id>/', ExerciseViews.exercise_detail, name='exercise_detail'),
    path('pushup-counter/', ExerciseViews.pushup_counter_view, name='pushup-counter'),
    path('event/', include('EventApp.urls')),
    path('mental/', include('MentalApp.urls')),
    path('meal/', include('MealApp.urls')),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
