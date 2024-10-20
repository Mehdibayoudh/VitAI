from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from bson import ObjectId

from .models import SportEvent
# Create your views here.



def delete_event(request, idEvent):
    if request.method == "POST":
        event = SportEvent.objects.get(id=idEvent)
        event.delete()  # Delete the user if found
        return redirect('allEvents')  # If event doesn't exist, redirect
    return redirect('allEvents')  # If event doesn't exist, redirect


def update_event(request, idEvent):
    event = SportEvent.objects.get(id=idEvent)

    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        location = request.POST.get('location')
        participants = request.POST.get('participants')

        if not (name and date and location and participants):
            # If any field is missing, return an error or show a message
            return render(request, 'update-event.html', {'event': event, 'error': 'Please fill in all fields.'})

        # Update the event with the new data
        event.name = name
        event.date = date
        event.location = location
        event.participants = participants
        event.save()
        return redirect('allEvents')  # Redirect to the list of events



def all_events(request):
    events = SportEvent.objects.all()
    return render(request, 'all-events.html', {'events': events})



def create_event(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        location = request.POST.get('location')
        participants = request.POST.get('participants')

        # You can add basic validation here if needed
        if name and date and location and participants:
            event = SportEvent(
                name=name,
                date=date,
                location=location,
                participants=int(participants)
            )
            event.save()
            return redirect('allEvents')
        else:
            return HttpResponse('Please fill all fields')

    return render(request, 'add-event.html')

