from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/',views.UserLogin.as_view(),name='login'),
    path('logout/',views.UserLogout.as_view(),name='logout'),
    path('register/',views.UserRegister.as_view(),name='register'),

]