from ast import If
from contextlib import redirect_stderr
import email
from email import message
from telnetlib import LOGOUT
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

import authentication


# Create your views here.
def home(request):
    return render(request, 'authentication/index.html')


def signup(request):

    if request.method == 'POST':
        #username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, 'Username alredy exist!')
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, 'Email alredy registered with!')
            return redirect('home')

        if len(username)>15:
            messages.error(request, 'Username must be under 15 characters!')

        if pass1 != pass2:
            messages.error(request, 'Passwords do not match!')


        if not username.isalnum():
            messages.error(request, 'Username must be Alpha-Numeric!')
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, 'Your Account Has Been Successfully Created')
        return redirect('signin')

    return render(request, 'authentication/signup.html')

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request, 'authentication/dashboard.html', {'fname':fname})
        else:
            messages.error(request, 'Bad Credentials')
            return redirect('home')

    return render(request, 'authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

def dashboard(request):
    return render(request, 'authentication/dashboard.html')