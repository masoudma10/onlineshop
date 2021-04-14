from django.contrib.auth.models import BaseUserManager



class MyUserManager(BaseUserManager):

    def create_user(self,email,fname,lname,phone,password):
        """

        :return:
        """
        if not email:
            raise ValueError('users must have Email')
        if not fname and lname:
            raise ValueError('users must have first name and last name')

        if not phone:
            raise ValueError('enter your phone number')

        user = self.model(email=self.normalize_email(email), fname=fname,
                          lname=lname, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user




    def create_superuser(self,email,fname,lname,phone,password):
        user = self.create_user(email,fname,lname,phone,password)
        user.is_admin = True
        user.save(using=self._db)