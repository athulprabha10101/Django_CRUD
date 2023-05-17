from django.urls import path
from . import views

urlpatterns = [
        path('', views.user_login, name='user_login'),
        
        path('signup', views.signup, name='signup'),
        path('user_home', views.user_home, name='user_home'),
        path('user_logout', views.user_logout, name='user_logout'),
        path('admin_home', views.admin_home, name='admin_home'),


    ]