from django.forms import ModelForm
from events.models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "city",
            "location",
            "date",
            "poster",
        ]

        labels = {
            "title": "Title",
            "description": "Description",
            "city": "City",
            "location": "Location",
            "date": "Date",
            "poster": "Poster",
        }
