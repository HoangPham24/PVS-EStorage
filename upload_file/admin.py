from django.contrib import admin
from .models import *

# Register your models here.

class GetApiAdmin(admin.ModelAdmin):
    
    model = GetApiPVS
    list_display = ['id', 'content', 'creator']


admin.site.register(GetApiPVS, GetApiAdmin)
admin.site.register(ExcelFile)