from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm

# Create your views here.
def signup(request):
    if request.method == 'POST': 
        form = CustomUserCreationForm(request.POST) # create an empty form containing data inputted by the user
        if form.is_valid():
            user = form.save() # create the user
            login(request, user) # login that user
            return redirect('homepage') #take user to homepage
        else:
            return render(request, 'accounts\signup.html', {'form': form}) #re render html page and display errors
    else:  # if method is a get
         form = CustomUserCreationForm() # create an empty form
         return render(request, 'accounts\signup.html', { # render the html file with that form 
             'form' : form
         })      

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, 'accounts\login.html', {'form': form}) #re render html page and display errors
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})   
       
def homepage(request):
        return HttpResponse("HomePage!")
