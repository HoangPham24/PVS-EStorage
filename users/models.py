from django.db import models
from django.conf import settings
import requests
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)


# Create your models here.



#Department models 
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


# Staff profile
class StaffProfile(models.Model):
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    joined = models.DateField(blank=True, null=True)
    contract = models.DateField(blank=True, null=True)
    position = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.name

    def is_deletable(self):
        for rel in self._meta.get_all_related_objects():
            if rel.model.objects.filter(**{rel.field.name: self}).exists():
                return False
        return True    
  


# Custom User manager
class UserManager(BaseUserManager):
    
    def _create_user(self, email, 
                    password, is_staff, is_superuser,**extra_fields):
        
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password,  is_superuser=False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, is_staff=True, 
                                is_superuser=True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user

# Custom User model
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField("email address", max_length=100, unique=True)
    is_staff = models.BooleanField("staff status", default=False,
                                   help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(
        "active", default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    is_admin = models.BooleanField(
        "admin PVS", default=False, help_text='Designates whether this user should be treated as admin. Admin can manage all staffs.')

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        try:
            return "{} - {}".format(self.email, self.staffprofile.name)
        except:
            return self.email


    