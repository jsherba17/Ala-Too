from django.urls import path
from .views import *
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('author/<str:username>', author, name='author'),
    path('register/', register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='user/logout.html'), name='logout'),


]
