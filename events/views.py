from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Event,MyUser
from django.contrib import messages
from .forms import EventForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from .forms import CustomUserCreationForm
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
                Q(promoter__username__icontains=query) |
                Q(event_type__icontains=query)
            )
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = Event.objects.order_by().values_list('city', flat=True).distinct()
        context['event_types'] = self.model.objects.order_by().values_list('event_type', flat=True).distinct()
        context['locations'] = Event.objects.values_list('city', flat=True).distinct()
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

class SearchView(TemplateView):
    template_name = 'events/search_results.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if query:
            object_list = Event.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(city__icontains=query) |
                Q(location__icontains=query) |
                Q(event_type__icontains=query)
            )
        else:
            object_list = Event.objects.none()

        return self.render_to_response({'object_list': object_list, 'query': query})


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
    # Check if the user is authenticated and is 1a promoter
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
        else:
            form = EventForm(instance=event)
        return render(request, "edit_event.html", {"form": form, "event": event})
    else:
        messages.warning(request, "You don't have permission to edit this event.")
        return redirect("/")


def homepage(request):
    allevents = Event.objects.all()
    query = request.GET.get('q')
    if query:
        events = Event.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(city__icontains=query) |
            Q(location__icontains=query) |
            Q(event_type__icontains=query)
        )
    else:
        events = Event.objects.none()

    return render(request, '', {'user': MyUser, 'events': events, 'query': query, 'allevents': allevents})

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
    return render(request, 'templates/myaccount.html', {
        'user': MyUser
    })