from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from django.contrib.auth.models import User, auth
from django.views.decorators.cache import never_cache

# Create your views here.

@never_cache
def user_login(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_home')
        else:
            return redirect('user_home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user is not None and user.check_password(password):
            login(request, user)

            if user.is_superuser:
                return redirect('admin_home')
            else:
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
    if request.user.is_authenticated and not request.user.is_superuser:
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
    user_data = User.objects.all()
    search = request.POST.get('search')
    if search:
        details = User.objects.filter(username__istartswith=search)
    else:
        details = User.objects.all()
    return render(request, 'admin_home.html', {'user_data': details})


def edit_details(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        user = User.objects.get(id = id)
        return render(request, 'edit_details.html',{'user':user})
    
def update_details(request, id):
    print("hello")
    user = User.objects.get(id=id)
    if request.method == 'POST':
        
        user.first_name = request.POST.get('name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        return redirect('admin_home')
    
    return render(request, 'edit_details.html', {'user': user})


def delete_details(request, id):
    user = User.objects.get(id = id)
    user.delete()
    return redirect('admin_home')

def add_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        
        if password == cpassword: 
            if User.objects.filter(username = username).exists():
                return render(request, 'signup.html',{'pw_error': 'Password mismatch','taken': 'Username taken'})
            if User.objects.filter(email = email):
                return render(request, 'signup.html''signup.html',{'pw_error': 'Email already registered'})
            else:
                User.objects.create_user(first_name = name, username = username, email = email, password = password).save()
                return redirect('admin_home')
        else:
            return render(request, 'signup.html',{'pw_error': 'Password mismatch'}) 
    return render(request, 'add_user.html')

