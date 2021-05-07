from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.signals import post_save

from .managers import MyUserManager


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phone = models.PositiveBigIntegerField(null=True,blank=True,unique=True)

    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    # to authenticate users
    USERNAME_FIELD = 'email'

    # for create superuser
    REQUIRED_FIELDS = ['fname', 'lname','phone',]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    # can user permissions to read models
    def has_module_perms(self, app_label):
        if self.is_admin:
            return True

    # users can be staff
    def is_staff(self):

        return self.is_admin




class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    address = models.TextField(blank=True,null=True)
    home_phone = models.PositiveIntegerField(null=True,blank=True)
    code_melli = models.PositiveIntegerField(null=True,blank=True)
    code_post = models.PositiveIntegerField(null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)




def save_profile(sender,**kwargs):
    if kwargs['created']:
        p1 = Profile(user=kwargs['instance'])
        p1.save()



post_save.connect(save_profile,sender=User)
