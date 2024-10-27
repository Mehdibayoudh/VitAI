from django.urls import path
from . import views

urlpatterns = [

    path('allEvents', views.all_events, name='allEvents'),
    path('addEvent', views.create_event, name='addEvent'),

]
