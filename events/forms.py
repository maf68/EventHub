from django import forms
from django.forms.widgets import TextInput
from events.models import Event

class DurationInput(TextInput):
    input_type = 'duration'

class EventForm(forms.ModelForm):
    duration = forms.DurationField(widget=DurationInput)

    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "city",
            "location",
            "date",
            "poster",
            "duration"
        ]

        labels = {
            "title": "Title",
            "description": "Description",
            "city": "City",
            "location": "Location",
            "date": "Date",
            "poster": "Poster",
            "duration": "Duration"
        }