from django.urls import path
from . import views

urlpatterns = [
        path('', views.user_login, name='user_login'),
        path('signup', views.signup, name='signup'),
        path('user_home', views.user_home, name='user_home'),
        path('user_logout', views.user_logout, name='user_logout'),
        path('admin_home', views.admin_home, name='admin_home'),
        path('edit_details<int:id>', views.edit_details, name = 'edit_details'),
        path('update_details<int:id>', views.update_details, name = 'update_details'),
        path('delete_details<int:id>', views.delete_details, name = 'delete_details'),
        path('add_user', views.add_user, name = 'add_user'),
        
    ]