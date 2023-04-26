from django import forms
from .models import Review
from django.forms.widgets import TextInput
from events.models import Event, MyUser
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
import re;
from django.contrib.auth.hashers import make_password

class MyUserForm(forms.ModelForm):
        is_promoter = forms.ChoiceField(choices=((False, 'Normal User'), (True, 'Promoter')), label='User Type')
        password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave empty to not change the password")
        class Meta:
            model = MyUser
            fields = ['first_name', 'last_name', 'date_of_birth', 'nationality', 'address', 'is_promoter', 'bio', 'picture', 'password']
            widgets = {
                'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
                'nationality': forms.Select(attrs={'class': 'custom-select'}),
                'address': forms.TextInput(attrs={'class': 'form-control'}),
                'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                'picture': forms.URLInput(attrs={'class': 'form-control'}),
            }
        def __init__(self, *args, **kwargs):
            super(MyUserForm, self).__init__(*args, **kwargs)
            self.fields['password'].widget.attrs.update({'class': 'form-control'})
            self.fields['is_promoter'].widget.attrs.update({'class':'form-control'})
        def clean_password(self):
            password = self.cleaned_data.get('password')
            if password:
                return make_password(password)
            else:
                return self.instance.password
 
class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent')
    ]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect) 
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), max_length=500)

    class Meta:
        model = Review
        fields = ('rating', 'comment',)
    
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if int(rating) not in [choice[0] for choice in self.RATING_CHOICES]:
            raise forms.ValidationError("Invalid rating value")
        return rating
    
    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if not comment:
            raise forms.ValidationError("Comment cannot be empty")
        return comment
    
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


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='*')
    last_name = forms.CharField(max_length=30, required=True, help_text='*')
    date_of_birth = forms.CharField(max_length=30, required=True, help_text='*')
    nationality = CountryField().formfield()
    bio = forms.CharField(max_length=200)
    picture = forms.URLInput()
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        min_length=5,
        help_text=(" * "),
        error_messages={
            'min_length': ("Your password must contain at least 8 characters."),
            'required': ("Please enter a password."),
        },
    )
    email = forms.EmailField(max_length=30, required=True)

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
  
    is_promoter = forms.BooleanField(
        label=("Is Promoter"),
        required = False
    )
    def __init__(self, *args, **kwargs):
            super(CustomUserCreationForm, self).__init__(*args, **kwargs)
            self.fields['picture'].widget.attrs.update({'style':'display: block; width: 100%; padding: 10px; margin-bottom: 20px; font-size: 18px; border-radius: 5px; border: 2px solid #ddd;'})
    def validate_password(password1):
    # Check for a minimum length of 8 characters
        if len(password1) < 6:
            raise ValidationError('Password must be at least 5 characters long.')
    # Check for at least one uppercase letter, one lowercase letter, one digit, and one special character
        if not re.search(r'[A-Z]', password1):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', password1):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'\d', password1):
            raise ValidationError('Password must contain at least one digit.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
           pass

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'email', 'picture', 'nationality','bio', 'is_promoter', 'date_of_birth', 'password1','password2')
