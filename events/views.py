from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Event, Review, MyUser
from .forms import ReviewForm
from django.urls import reverse
from django.contrib import messages
from .forms import EventForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from .forms import CustomUserCreationForm
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Event, Review, MyUser, Announcement
from .forms import ReviewForm, MyUserForm
from django.urls import reverse
from django.contrib import messages
from .forms import EventForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from eventhub.settings import BASE_URL
from django.forms import ValidationError;
from django.utils import timezone


# def event_reviews(request, id):
#     event = get_object_or_404(Event, id=id)
#     reviews = Review.objects.filter(event=event).order_by('-created_at')
#     context = {'event': event, 'reviews': reviews}
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.event = event
#             review.user = request.user
#             review.comment = form.cleaned_data['comment']
#             review.save()
#             reviews_url = reverse('events:event_reviews', args=[event.id]) + '?reviews=1'
#             return redirect(reviews_url)
#             # return redirect('events:event_reviews', event.id)
        
#         else:
#             context['form'] = form
#             context['form_errors'] = form.errors
#     else:
#         form = ReviewForm()
#         context['form'] = form 

#     # If the updated reviews list is included in the query parameters,
#     # retrieve the updated reviews list and include it in the context
#     if 'reviews' in request.GET:
#         updated_reviews = Review.objects.filter(event=event).order_by('-created_at')
#         context['reviews'] = updated_reviews
        
#     return render(request, 'events/event_reviews.html', context)


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(city__icontains=query) |
                Q(location__icontains=query) |
                Q(promoter_username_icontains=query) |
                Q(event_type__icontains=query)
            )
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = Event.objects.order_by().values_list('city', flat=True).distinct()
        context['event_types'] = self.model.objects.order_by().values_list('event_type', flat=True).distinct()
        context['locations'] = Event.objects.values_list('city', flat=True).distinct()
        context['today'] = timezone.datetime.today().date

        return context

class EventSearchView(ListView):
    model = Event
    template_name = 'events/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query and query.strip():
            object_list = Event.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(city__icontains=query) |
                Q(location__icontains=query) |
                Q(event_type__icontains=query) |
                Q(date__icontains=query) |
                Q(duration__icontains=query)
            )
            return object_list
        else:
            return Event.objects.none()

class EventFilterView(ListView):
    model = Event
    template_name = 'events/event_filter.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = super().get_queryset()
        location = self.request.GET.get('location')
        date = self.request.GET.get('date')
        duration = self.request.GET.get('duration')
        event_type = self.request.GET.get('event_type')

        if location:
            queryset = queryset.filter(city=location)
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                queryset = queryset.filter(date__gte=date_obj)
            except ValueError:
                pass
        if duration:
            try:
                duration_list = duration.split(':')
                hours = int(duration_list[0])
                minutes = int(duration_list[1])
                seconds = int(duration_list[2]) if len(duration_list) > 2 else 0
                duration_obj = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                queryset = queryset.filter(duration__gte=duration_obj)
            except (ValueError, IndexError):
                pass
    
        if event_type:
            queryset = queryset.filter(event_type=event_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = Event.objects.order_by('city').values_list('city', flat=True).distinct()
        context['event_types'] = self.model.objects.order_by('event_type').values_list('event_type', flat=True).distinct()
        return context

def create_event(request):
    # print(request.user.is_authenticated)  # is logged in
    if request.user.is_authenticated and request.user.is_promoter:
        user = (
            request.user._wrapped if hasattr(request.user, "_wrapped") else request.user
        )
        # print("PROMOTER %s " % request.user.id)
        if request.method == "POST":
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.promoter = user
                event.save()
                return redirect("/")
            else:
                return render(request, "createevent.html", {"form": form})
        else:
            form = EventForm()
            return render(request, "createevent.html", {"form": form})
    else:
        return redirect("/")


def edit_event(request, event_id):
    # Check if the user is authenticated and is a promoter
    if request.user.is_authenticated and request.user.is_promoter:
        event = get_object_or_404(Event, id=event_id, promoter=request.user)
        if request.method == "POST":
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                messages.success(request, "Event updated successfully!")
                return redirect("/")
            else:
                messages.error(request, "Please correct the errors below.")
                #try:
                    #form.clean_duration()
                #except ValidationError as e:
                    #context = {
                    #'form': form,
                    #'error_message': str(e),
                    #}
                #return render(request, 'create_event.html', context=context)
        else:
            form = EventForm(instance=event)
        return render(request, "edit_event.html", {"form": form, "event": event})
    else:
        messages.warning(request, "You don't have permission to edit this event.")
        return redirect("/")
    
def signup(request):
    if request.method == 'POST': 
        form = CustomUserCreationForm(request.POST, request.FILES) # create a form containing data inputted by the user
        if form.is_valid():
            form.save() # create the user and save into database
            print(form.cleaned_data)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password) #authenticate username and password
            login(request, user) # login that user
            return redirect('/') #take user to homepage
        else:
            return render(request, 'events/signup.html', {'form': form}) #re render html page and display errors
    else:  # if method is a get
         form = CustomUserCreationForm() # create an empty form
         return render(request, 'events/signup.html', { # render the html file with that form 
             'form' : form
         })      
    
def login_(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) #create a form containing data inputted by user
        if form.is_valid():
            username = form.cleaned_data.get('username') #get username and pass in form
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password) #check if username and password in form match database
            if user is not None: #if match
                login(request, user) # login user and redirect to homepage
                return redirect('/')
            else:
                error_message = 'Invalid login credentials. Please try again.' # if no match, invalid
        else:
            error_message = 'Invalid login credentials. Please try again.'    # if invalid form, invalid     
    else:
        form = AuthenticationForm() # if get request, create an empty form for user to fill 
        error_message = None
    return render(request, 'events/login.html', {'form': form, 'error_message': error_message}) # render html form     

def logout_(request):
    print("logout")
    logout(request)
    return redirect('/')

def myaccount_view(request):
    return render(request, 'events/myaccount.html', {
        'user': MyUser
    })
# def event_detail(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     return render(request, 'event_detail.html', {'event': event})


def event_details_and_reviews(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reviews = Review.objects.filter(event=event).order_by('-created_at')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.event = event
            if request.user.is_authenticated:
                review.user = request.user
            else:
                review.user = MyUser.objects.get_or_create(username=settings.ANONYMOUS_USER_NAME)[0] # assign the anonymous user to the review    
            review.comment = form.cleaned_data['comment']
            review.save()
            reviews_url = reverse('event_details_and_reviews', args=[event.id]) + '?reviews=1'
            return redirect(reviews_url)
        else:
            context = {'event': event, 'reviews': reviews, 'form': form, 'form_errors': form.errors}
            return render(request, 'event_details_and_reviews.html', context)
    else:
        form = ReviewForm()
        context = {'event': event, 'reviews': reviews, 'form': form, 'user':request.user}

    # If the updated reviews list is included in the query parameters,
    # retrieve the updated reviews list and include it in the context
    if 'reviews' in request.GET:
        updated_reviews = Review.objects.filter(event=event).order_by('-created_at')
        context['reviews'] = updated_reviews

    return render(request, 'event_details_and_reviews.html', context)


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
    return render(request, 'event_announcements.html', context)

#Create an announcement.
def create_announcement(request, Event_id):
    event = get_object_or_404(Event, id=Event_id)
    if (request.user.is_authenticated == False) or (event.promoter != request.user):
        return redirect('/')
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
            return redirect('/')
    
    return render(request, 'create_announcement.html', {'event': event})

#Probably better to make an edit announcement in the future.

#Announcement details.
def Announcement_by_id(request, Announcement_id):
    announcement = Announcement.objects.get(pk = Announcement_id)
    return render(request, 'announcement_details.html', {'Announcement': announcement})    

def profile(request):
    if (request.user.is_authenticated):
        user = request.user
        return render(request, 'profile.html', {'user': user})
    return redirect('/')

def privacy_policy(request):
    return render(request, 'privacy.html', {})

def terms(request):
    return render(request, 'terms.html', {})

def settings_(request):
    user = request.user
    if (user.is_authenticated):
        if request.method == 'POST':
            form = MyUserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('/')
        else:
            form = MyUserForm(instance=user)
        return render(request, 'settings.html', {'form': form})
    return redirect("/")

def follow_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user
    if user.is_authenticated:
        event.following.add(user)
        event.save()
        return redirect("/")
    else:
        # Do something like redirect to the login page
        return redirect("/")

def followed_events(request):
    # Get the current user
    user = request.user
    
    # Get all the events the user is following
    followed_events = Event.objects.filter(following__in=[user])
    
    # Render the events using a template
    context = {'followed_events': followed_events}
    return render(request, 'followed_events.html', context)
