from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, auth
from django.views.decorators.cache import never_cache

from app_crud.models import custom_user

# Create your views here.

@never_cache
def user_login(request):

    if 'username' in request.session:
        username =request.session['username']
        user = custom_user.objects.get(username=username)
    
        if user.is_superuser:
            return redirect('admin_home')
        else:
            return redirect('user_home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = custom_user.objects.filter(username=username, password = password).first()
     
        if user is not None:
            
            print(user.username)
            
            request.session["username"] = username

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
            if custom_user.objects.filter(username = username).exists():
                return render(request, 'signup.html''signup.html',{'pw_error': 'Password mismatch','taken': 'Username taken'})
            if custom_user.objects.filter(email = email):
                return render(request, 'signup.html''signup.html',{'pw_error': 'Email already registered'})
            else:
                custom_user(first_name = name, username = username, is_superuser = True, email = email, password = password).save()
                return redirect('user_login')
        else:
            return render(request, 'signup.html',{'pw_error': 'Password mismatch'}) 
            
    return render(request, 'signup.html')

@never_cache
def user_home(request):
    if 'username' in request.session: 
        username =request.session['username']
        user = custom_user.objects.get(username=username)
        
        if not user.is_superuser:
            return render (request, 'user_home.html')
        else: return redirect('user_login')
    
    return redirect('user_login')

@never_cache
def user_logout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect('user_login')

@never_cache
def admin_home(request):
  
  if 'username' in request.session: 
    username =request.session['username']
    user = custom_user.objects.get(username=username)
    if user.is_superuser:

        user_data = custom_user.objects.all()
        search = request.POST.get('search')
        if search:
            details = custom_user.objects.filter(username__istartswith=search)
        else:
            details = custom_user.objects.filter(is_superuser=False)
        return render(request, 'admin_home.html', {'user_data': details})
    else: return redirect('user_login')

def edit_details(request, id):
    
    if 'username' in request.session:
        user = custom_user.objects.get(id = id)
        return render(request, 'edit_details.html',{'user':user})
    
def update_details(request, id):
    
    user = custom_user.objects.get(id=id)
    if request.method == 'POST':
        
        user.first_name = request.POST.get('name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        return redirect('admin_home')
    
    return render(request, 'edit_details.html', {'user': user})


def delete_details(request, id):
    user = custom_user.objects.get(id = id)
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
            if custom_user.objects.filter(username = username).exists():
                return render(request, 'signup.html',{'pw_error': 'Password mismatch','taken': 'Username taken'})
            if custom_user.objects.filter(email = email):
                return render(request, 'signup.html',{'pw_error': 'Email already registered'})
            else:
                custom_user(first_name = name, username = username, email = email, password = password).save()
                return redirect('admin_home')
        else:
            return render(request, 'signup.html',{'pw_error': 'Password mismatch'}) 
    return render(request, 'add_user.html')

