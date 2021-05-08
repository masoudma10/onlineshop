from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserLoginForm,UserRegisterForm,EditProfileForm,PhoneLoginForm,VerifyCodeForm
from .models import User,Profile
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from random import randint
from kavenegar import *

class UserRegister(View):
	form_class = UserRegisterForm
	template_name = 'accounts/register.html'

	def get(self, request):
		form = self.form_class
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = User.objects.create_user(cd['email'], cd['fname'], cd['lname'], cd['phone'], cd['password'])
			user.save()
			messages.success(request, 'you registered successfully', 'info')
			return redirect('shop:home')
		return render(request, self.template_name, {'form':form})


class UserLogin(View):
	form_class = UserLoginForm
	template_name = 'accounts/login.html'

	def get(self, request):
		form = self.form_class
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd['email'], password=cd['password'])
			if user is not None:
				login(request, user)
				messages.success(request, 'you logged in successfully', 'info')
				return redirect('shop:home')
			messages.error(request, 'username or password is wrong', 'warning')
		return render(request, self.template_name, {'form':form})




class UserLogout(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		messages.success(request, 'you logged out successfully', 'info')
		return redirect('shop:home')



class UserPassReset(auth_views.PasswordResetView):
	template_name = 'accounts/password_reset_form.html'
	success_url = reverse_lazy('accounts:password_reset_done')
	email_template_name = 'accounts/password_reset_email.html'


class PasswordResetDone(auth_views.PasswordResetDoneView):
	template_name = 'accounts/reset_done.html'



class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
	template_name = 'accounts/password_reset_confirm.html'
	success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetComplete(auth_views.PasswordResetCompleteView):
	template_name = 'accounts/password_reset_complete.html'

@login_required
def user_dashboard(request,user_id):
	user = get_object_or_404(User,id=user_id)

	self_dash = False
	if request.user.id == user_id:
		self_dash = True
	return render(request,'accounts/dashboard.html',{'user':user,'self_dash':self_dash})

@login_required
def edit_profile(request,user_id):
	user = get_object_or_404(User,pk=user_id)
	if request.method == 'POST':
		form = EditProfileForm(request.POST,instance=user.profile)
		if form.is_valid():
			form.save()
			messages.success(request,'your profile edited successfully','success')
			return redirect('accounts:user_dashboard',user_id)
	else:
		form = EditProfileForm(instance=user.profile)
		return render(request,'accounts/edit_profile.html',{'form':form})


def phone_login(request):
	if request.method == 'POST':
		form = PhoneLoginForm(request.POST)
		if form.is_valid():
			phone = f"0{form.cleaned_data['phone']}"
			rand_num = randint(1000,9999)
			api = KavenegarAPI('785A784533315867732B6C6E754E4635676F463175515A52376634327A61746F4E6A3966362F38534A4E773D',)
			params = {'sender': '', 'receptor': phone, 'message': f'login code: {rand_num}',}
			api.sms_send(params)
			return redirect('accounts:verify', phone,rand_num)

	else:
		form = PhoneLoginForm()

	return render(request,'accounts/phone_login.html',{'form':form})


def verify(request,phone,rand_num):
	if request.method == 'POST':
		form = VerifyCodeForm(request.POST)
		if form.is_valid():
			if rand_num == form.cleaned_data['code']:
				user = get_object_or_404(User,phone=phone)

				login(request,user)
				messages.success(request,'logged in successfully' 'success')
				return redirect('shop:home')
			else:
				messages.error(request,'Wrong code','danger')
	else:
		form = VerifyCodeForm()
		return render(request,'accounts/verify.html',{'form':form})



















