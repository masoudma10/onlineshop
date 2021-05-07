from django import forms
from .models import User,Profile
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','fname','lname','phone')


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise forms.ValidationError('passwords must match')
        return cd['password2']


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email','password','fname','lname','phone')


        def clean_password(self):
            return self.initial['password']



class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class UserRegisterForm(forms.Form):
    fname = forms.CharField(label='first name:',widget=forms.TextInput(attrs={'class':'form-control'}))
    lname = forms.CharField(label='last name',widget=forms.TextInput(attrs={'class':'form-control'}))
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class':'form-control'}))



    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password2'] and cd['password'] != cd['password2']:
            raise forms.ValidationError('passwords must match')
        return cd['password2']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address','home_phone','date_of_birth','code_melli','code_post')







