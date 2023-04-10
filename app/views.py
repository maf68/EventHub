from django.shortcuts import render
from django.http import HttpResponse
from .models import Event
from .models import MyUser
from .models import Announcement
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
#Testing function
def Index(request):
    return HttpResponse("Hello World.")
#Testing events model, can be used as a basis for event details.
def Event_by_id(request, Event_id):
    event = Event.objects.get(pk = Event_id)
    return render(request, 'Event_details.html', {'event': event})
#Testing announcement model
def Announcement_by_id(request, Announcement_id):
    announcement = Announcement.objects.get(pk = Announcement_id)
    return render(request, 'Announcement_details.html', {'Announcement': announcement})    

#Display all announcements for an event
def get_event_announcements(request, Event_id):
    # Get the event object based on the event_id parameter
    event = get_object_or_404(Event, id=Event_id)

    # Get all the announcements for the event
    announcements = Announcement.objects.filter(event=event)

    # Render the announcements in a template or return as JSON
    context = {
        'event': event,
        'announcements': announcements,
    }
    return render(request, 'Event_announcements.html', context)

#Create an announcement.
@login_required
def create_announcement(request, Event_id):
    event = get_object_or_404(Event, id=Event_id)

    #if request.MyUser != event.promoter:
    #    return HttpResponseBadRequest("You're not authorized to create announcements for this event.")

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.POST.get('image')

        if title and description:
            announcement = Announcement.objects.create(
                title=title,
                description=description,
                image=image,
                event=event
            )
            followers = event.following.all()
            subject = f'New announcement for {event.title}'
            message = f'There is a new announcement for {event.title}:\n\nTitle: {announcement.title}\nDescription: {announcement.description}\n\n'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [follower.email for follower in followers]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            #Needs to be updated to redirect to the url for the event details.
            return render(request, 'Event_details.html', {'event': event})
            #return HttpResponseRedirect(reverse('Event', args=[event.id]))
    
    return render(request, 'Create_announcement.html', {'event': event})

#Probably better to make an edit announcement in the future.