from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .forms import SignUpForm, LoginForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                user = User.objects.create_user(username = form.cleaned_data['username'],
                                                password = form.cleaned_data['password'])
                username1 = request.POST.get('username')                               
                auth.login(request, user)
                messages.success(request, "Welcome %s"%username1)
                return redirect('home')
            else:
                messages.warning(request, 'Password must match')
                return redirect('signup')
        else:
            username1 = request.POST.get('username')
            messages.warning(request, 'Username %s already exists'%username1)
            return redirect('signup')
    else:
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = auth.authenticate(username = request.POST.get('username'),
                                password = request.POST.get('password'))
        if user is not None:
            auth.login(request, user)
            username1 = request.user.username
            messages.success(request, "Welcome %s"%username1)
            return redirect('home')
        else:
            messages.warning(request, "Username or Password is invalid")
            return redirect('login')
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})


def logout(request):
    if request.method == 'POST':
        username1 = request.user.username
        auth.logout(request)
        messages.success(request, '%s Logged out Successfully'%username1)
        return redirect('home')








