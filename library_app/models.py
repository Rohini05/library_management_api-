
# from mynetwork.models import Group_Post
from os import read


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

from django.contrib.auth.models import Group, Permission


# Create your models here.
import re

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

class MyAccountManager(BaseUserManager):

    def create_user(self, email, contact_number, password, **other_fields):
        print("hello")
        if not email:
            raise ValueError('Users must have an email address')

        if not contact_number:
            raise ValueError('Users must have a mobile number')

        email = self.normalize_email(email)    
        user = self.model(email=email, contact_number=contact_number, **other_fields)

        user.set_password(password)
        # user.save(using=self._db)
        user.save()
        return user

    def create_superuser(self, email, contact_number, password, **other_fields):
       
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_admin', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, contact_number, password, **other_fields)



class MyUser(AbstractBaseUser):
    username                    = models.CharField(max_length=200)
    email                       = models.EmailField(verbose_name="email", max_length=80,unique=True)
    contact_number              = models.CharField(max_length=15, validators=[RegexValidator(regex='^.{10}$', message='Mobile Number Length has to be 10', code='nomatch')])
    date_joined                 = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    is_admin                    = models.BooleanField(default=False)
    is_active                   = models.BooleanField(default=True)
    is_staff                    = models.BooleanField(default=False)
    is_superuser                = models.BooleanField(default=False)
   
    
   
    groups = models.ManyToManyField(
        Group,
        help_text='Highlighted groups are the ones this user is a member of.',
        blank=True
    )

    #did not use permission
    permissions = models.ManyToManyField(
        Permission,
        help_text='Highlighted permissions are the ones this user is a member of.',
        blank=True
    )
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['contact_number', 'username']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True




class Library(models.Model):
   isbn                 = models.CharField(max_length=200)
   book_title           = models.CharField(max_length=200)
   author               = models.CharField(max_length=200)
   total_copies         = models.IntegerField(default=0)
   availables_copies    = models.IntegerField(default=0)
   user                = models.ForeignKey(MyUser,on_delete=models.CASCADE,blank=True,null=True)


