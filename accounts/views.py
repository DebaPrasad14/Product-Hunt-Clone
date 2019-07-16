from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def signup(request):

    if request.method=='POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1==password2:
            try:
                user = User.objects.get(username=username)
                context = 'Username has already been taken!'
                return render(request, 'accounts/signup.html', {'error':context})
            except User.DoesNotExist:
                user = User.objects.create_user(username, password=password1)
                auth.login(request, user)
                return redirect('home')
        else:
            context = 'Passwords must match!'
            return render(request, 'accounts/signup.html', {'error':context})

    return render(request, 'accounts/signup.html')


def login(request):

    username = request.POST.get('username')
    password = request.POST.get('password')

    if request.method=='POST':
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            context = 'Username or Password is incorrect'
            return render(request, 'accounts/login.html', {'error':context})
    return render(request, 'accounts/login.html')


def logout(request):
    if request.method=='POST':
        auth.logout(request)
        return redirect('home')
