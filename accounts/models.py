from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, phone_number, email, password=None, username=None, first_name=None, last_name=None):
        if not phone_number:
            raise ValueError('User must have a phone number')
        
        if email and Account.objects.filter(email=email).exists():
            raise ValueError('Email is already in use')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, email, password=None, username=None, first_name=None, last_name=None):
        user = self.create_user(
            phone_number=phone_number,
            email=email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    
    username  =models.CharField(max_length=50,blank=True, null=True)
    email  =models.EmailField(max_length=100,unique=True,blank=True, null=True)
    phone_number  =models.CharField(max_length=50,unique=True)
    first_name = models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50,blank=True,null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_login = models.DateTimeField(auto_now_add=True)
    is_admin    =models.BooleanField(default=False)
    is_staff    =models.BooleanField(default=False)
    is_active    =models.BooleanField(default=False)
    is_superadmin    =models.BooleanField(default=False)
    
    objects = MyAccountManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']
    def __str__(self):
        return self.phone_number
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True