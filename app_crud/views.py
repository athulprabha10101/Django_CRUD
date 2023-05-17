from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from django.contrib.auth.models import User, auth
from django.views.decorators.cache import never_cache

# Create your views here.

@never_cache
def user_login(request):
    if request.user.is_authenticated:
        return redirect('user_home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username = username, password = password) 
        if user is not None and user.is_superuser:
            login(request,user)
            return redirect ('admin_home')

        elif user is not None:
            login(request,user)
            return redirect('user_home')

    return render(request, 'login.html')

@never_cache
def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        
        if password == cpassword: 
            if User.objects.filter(username = username).exists():
                return render(request, 'signup.html''signup.html',{'pw_error': 'Password mismatch','taken': 'Username taken'})
            if User.objects.filter(email = email):
                return render(request, 'signup.html''signup.html',{'pw_error': 'Email already registered'})
            else:
                User.objects.create_user(first_name = name, username = username, email = email, password = password).save()
                return redirect('user_login')
        else:
            return render(request, 'signup.html',{'pw_error': 'Password mismatch'}) 
            
    return render(request, 'signup.html')

@never_cache
def user_home(request):
    if request.user.is_authenticated:
        return render (request, 'user_home.html')
    return redirect('user_login')

@never_cache
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('user_login')

@never_cache
def admin_home(request):
  if request.user.is_authenticated and request.user.is_superuser:
    return render (request, 'admin_home.html')

