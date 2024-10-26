from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('allEvents', views.all_events, name='allEvents'),
    path('addEvent', views.create_event, name='addEvent'),
    path('generate-event-description/', views.generate_description, name='generate_description'),
    path('<str:event_id>/', views.event_detail, name='event_detail'),

    path('delete/<str:idEvent>/', views.delete_event, name='delete_event'),  # Accept ObjectId as string
    path('update/<str:idEvent>/', views.update_event, name='update_event'),  # Accept ObjectId as string

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
