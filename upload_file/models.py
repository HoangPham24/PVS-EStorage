from django.db import models
from users.models import User
from django.core.validators import MinValueValidator


# Create your models here.

class GetApiPVS(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

class ExcelFile(models.Model):
    file = models.FileField(upload_to="media")    