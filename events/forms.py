from django import forms
from django.forms.widgets import TextInput

class DurationInput(TextInput):
    input_type = 'duration'

class EventForm(forms.ModelForm):
    duration = forms.DurationField(widget=DurationInput)

    class Meta:
        model = Event
        fields = ['location', 'date', 'duration', 'event_type']