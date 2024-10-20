from django.urls import path
from . import views

urlpatterns = [

    path('allEvents', views.all_events, name='allEvents'),
    path('addEvent', views.create_event, name='addEvent'),

    path('delete/<str:idEvent>/', views.delete_event, name='delete_event'),  # Accept ObjectId as string
    path('update/<str:idEvent>/', views.update_event, name='update_event'),  # Accept ObjectId as string

]
