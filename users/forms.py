from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from django.urls import reverse_lazy as _
from .models import User




class AdminUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email','is_staff','is_active','is_admin')

class AdminUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email','is_staff','is_active','is_admin','password')