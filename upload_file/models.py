from django.db import models
from users.models import User
from django.core.validators import MinValueValidator


# Create your models here.

class GetApi(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)
    stt = models.IntegerField(validators=[MinValueValidator(0)])
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True) 
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)