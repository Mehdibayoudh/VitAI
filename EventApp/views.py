import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from bson import ObjectId
import torch
from .models import SportEvent
from django.core.files.storage import default_storage
import os
from django.http import JsonResponse

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import requests

import logging
import base64
from django import template
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)

# Initialize the model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to("cuda" if torch.cuda.is_available() else "cpu")

register = template.Library()


def generate_description(request):
    if request.method == "POST":
        image_file = request.FILES.get('image')

        if image_file:
            # Load the image for processing
            image = Image.open(image_file).convert("RGB")
            description = ai_generate_description(image)  # Pass the image directly

            return JsonResponse({'description': description})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def ai_generate_description(image):
    # Process the image and generate a description
    text = "event of"
    #place = "the location of the event is :"
    inputs = processor(image, text, return_tensors="pt").to(model.device)

    # Generate caption
    output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption


def create_event(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        location = request.POST.get('location')
        participants = request.POST.get('participants')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        owner_id = "6713f6836794bd0178dc02dd"

        # You can add basic validation here if needed
        if name and date and location and participants:

            #
            # Generate the caption
            event = SportEvent(
                name=name,
                date=date,
                location=location,
                participants=int(participants),
                description=description,
                image = image,
                owner=owner_id


            )
            event.save()
            return redirect('allEvents')
        else:
            return HttpResponse('Please fill all fields')

    return render(request, 'add-event.html')



def event_detail(request, event_id):
    event = SportEvent.objects.get(id=event_id)
    remaining_places = event.participants - event.AlreadyParticipated


    return render(request, 'event-details.html', {'event': event,'remaining_places':remaining_places,'userId':"6713f6836794bd0178dc02dd"})


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
    print(torch.cuda.is_available())  # should return True if CUDA is available
    return render(request, 'all-events.html', {'events': events,'userId':"6713f6836794bd0178dc02dd"})



def participate_in_event(request, event_id):
    event = SportEvent.objects.get(id=event_id)
    user_id = "6713f6836794bd0178dc02dd"  # Assuming the user is authenticated

    if user_id not in event.participants_list:
        event.participants_list.append(user_id)
        event.AlreadyParticipated += 1
        event.save()

    return redirect('event_detail', event_id=event_id)  # Redirect to the event details page

