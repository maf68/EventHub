from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from events.models import MyUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='*')
    last_name = forms.CharField(max_length=30, required=True, help_text='*')
    date_of_birth = forms.CharField(max_length=30, required=True, help_text='*')
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        min_length=8,
        help_text=(" * "),
        error_messages={
            'min_length': ("Your password must contain at least 8 characters."),
            'required': ("Please enter a password."),
        },
    )

    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=(" * "),
        error_messages={
            'required': ("Please confirm your password."),
        },
    )
    username = forms.CharField(
        label=("Username"),
        strip=False,
        min_length=5,
        help_text=(" * "),
        error_messages={
            'min_length': ("Your username must contain at least 5 characters."),
            'required': ("Please enter a username."),
        },
    )
    role_choices = [('Attendee',' Attendee'),('Promoter','Promoter')]
    is_promoter = forms.ChoiceField(
        label= ("Choose Your Category * "),
        choices=role_choices,
        widget=forms.RadioSelect(attrs={'class':'radio-label'}), # attribute it to a radio label here so i can style it in my css as so
    )
    
    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'date_of_birth', 'is_promoter', 'password1', 'password2')
