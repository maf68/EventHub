from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from .forms import EventForm
from django.contrib import messages
from .models import Event


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
                return redirect("homepage")
            else:
                return render(request, "createevent.html", {"form": form})
        else:
            form = EventForm()
            return render(request, "createevent.html", {"form": form})
    else:
        form = EventForm()
        return render(request, "createevent.html", {"form": form})


def edit_event(request, event_id):
    # Check if the user is authenticated and is a promoter
    if request.user.is_authenticated and request.user.is_promoter:
        event = get_object_or_404(Event, id=event_id, promoter=request.user)
        if request.method == "POST":
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                messages.success(request, "Event updated successfully!")
                return redirect("homepage")
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = EventForm(instance=event)
        return render(request, "edit_event.html", {"form": form, "event": event})
    else:
        messages.warning(request, "You don't have permission to edit this event.")
        return redirect("homepage")


def homepage(request):
    return HttpResponse("HomePage")
