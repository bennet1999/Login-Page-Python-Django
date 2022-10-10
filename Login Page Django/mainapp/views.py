from ast import If
from contextlib import redirect_stderr
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def index(request):
    if 'username' in request.session:
        return redirect('dashboard') 
    else:
        return render(request, 'index.html')

def signup(request):
    if 'username' in request.session:
        return redirect('dashboard')
    else:
        if request.method == 'POST':

            username = request.POST['username']
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

            if pass1 == pass2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, '! ! Username already exists ! !')
                    return redirect('signup')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, '! ! Email already registered with ! !')
                    return redirect('signup')
                elif not username.isalnum():
                    messages.info(request, '! ! Username must be Alpha-Numeric ! !')
                    return redirect('signup')
                else:
                    myuser = User.objects.create_user(username, email, pass1)
                    myuser.first_name = fname
                    myuser.last_name = lname
                    myuser.save()
                    messages.info(request, 'Your Account Has Been Successfully Created.')
                    return redirect('signin')
            else:
                messages.info(request, "! ! Passwords not matching ! !")
                return redirect('signup')
        else:
            return render(request, 'signup.html')

def signin(request):
    if 'username' in request.session:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            pass1 = request.POST['pass1']

            user = auth.authenticate(username=username, password=pass1)

            if user is not None:
                login(request,user)
                request.session['username'] = username
                messages.info(request, 'Logged in Successfully')
                return render(request, 'dashboard.html')
            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('signin')
        else:  
            return render(request, 'signin.html')

def signout(request):
    if 'username' in request.session:
        request.session.flush()
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('index')


@login_required
def dashboard(request):
        return render(request, 'dashboard.html')