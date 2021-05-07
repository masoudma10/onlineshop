from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserLoginForm,UserRegisterForm,EditProfileForm
from .models import User,Profile
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy



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


















