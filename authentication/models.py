from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError(_('Please enter an email address'))

        email=self.normalize_email(email)

        new_user=self.model(email=email,**extra_fields)

        new_user.set_password(password)

        new_user.save()

        return new_user


    def create_superuser(self,email,password,**extra_fields):

        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))


        return self.create_user(email,password,**extra_fields)


class User(AbstractUser):
    GENDER = [
        ("UNSPECIFIED", "Unspecified"),
        ("MALE", "Male"),
        ("FEMALE", "Female"),
    ]

    username=None
    dateOfBirth = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=80, choices=GENDER, default="UNSPECIFIED")
    email = models.EmailField(unique=True,max_length=200)
    phone = models.CharField(max_length=18,null=True,blank=True)
    nid = models.CharField(max_length=200)
    f_id = models.IntegerField(null=True,blank=True)
    alternative_password = models.CharField(null=True,blank=True,max_length=500)
    state = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    country = models.CharField(max_length=255,null=True,blank=True)
    photo = models.ImageField(null=True,blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['first_name', 'last_name']
    objects = CustomUserManager()
    

    def __str__(self):
        return f"{self.email}"
