from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import SportEvent
# Create your views here.

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
