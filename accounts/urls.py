from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/',views.UserLogin.as_view(),name='login'),
    path('logout/',views.UserLogout.as_view(),name='logout'),
    path('register/',views.UserRegister.as_view(),name='register'),
    path('reset/',views.UserPassReset.as_view(),name='reset_pass'),
    path('reset/done/',views.PasswordResetDone.as_view(),name='password_reset_done'),
    path('confirm/<uidb64>/<token>/',views.PasswordResetConfirm.as_view(),name='password_reset_confirm'),
    path('confirm/done/',views.PasswordResetComplete.as_view(),name='password_reset_complete'),

]