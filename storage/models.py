
from xml.parsers.expat import model
from django.db import models
import os
from users.models import StaffProfile
from django.core.validators import MinValueValidator
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File

# Create your models here.



# locate img upload
def locate_img_upload(instance, filename):
    return os.path.join("assets-img/{}/{}".format(instance.sku,filename))
def locate_barcode_img_upload(instance, filename):
    return os.path.join("assets-img/{}/{}".format(instance.barcode, filename))

#Warehouse models
class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    # total_value = models.CharField(null=True, blank=True)
    address = models.TextField(blank=True, null=True,)
    
    def __str__(self):
        return self.name

#TypeAsset models
class TypeAsset(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
 
# Asset models
class Asset(models.Model):
    class Meta:
       ordering = ["id"]

    id = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=1000)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    detail = models.TextField(blank=True, null=True,)
    img = models.ImageField(upload_to=locate_img_upload, blank=True, null=True)
    type = models.ForeignKey(TypeAsset, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

    # #not allow delete ForeignKey
    # def is_deletable(self):
    #     for rel in self._meta.get_all_related_objects():
    #         if rel.model.objects.filter(**{rel.field.name: self}).exists():
    #             return False
    #     return True   
    

#Detail Asset Model
class AssetDetail(models.Model):
       
    id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    serial_no = models.CharField(max_length=200, blank=True, null=True)
    barcode = models.CharField(max_length=13, null=True, blank=True, unique=True)
    barcode_img = models.ImageField(upload_to=locate_barcode_img_upload,blank=True)
    purpose = models.TextField(blank=True, null=True,)
    active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    ip_source = models.CharField(max_length=100, null=True, blank=True)
    warranty_time = models. CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    dependency = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    description = models.TextField(blank=True, null=True,)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True, related_name='warehouse')
    commerce = models.BooleanField(default=False)
    
    def __str__(self):
        return "{} - {}".format(self.dependency, self.asset)
 
    # #not allow delete ForeignKey
    # def is_deletable(self):
    #     for rel in self._meta.get_all_related_objects():
    #         if rel.model.objects.filter(**{rel.field.id: self}).exists():
    #             return False
    #     return True 
        

    #generator barcode image
    def save(self, *args, **kwargs):         
        COD128 = barcode.get_barcode_class('code128')
        rv = BytesIO()
        code = COD128(f'{self.barcode}', writer=ImageWriter()).write(rv)
        self.barcode_img.save(f'{self.barcode}.png', File(rv), save=False)
        return super().save(*args, **kwargs)
            
        
 
#Timeline models
class Timeline(models.Model):
    class Meta:
        unique_together = ('detail_asset','manager', 'created_time', )
        ordering = ['created_time']

    id = models.AutoField(primary_key=True)
    detail_asset = models.ForeignKey(AssetDetail, on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.ForeignKey(StaffProfile, on_delete=models.PROTECT, null=True, blank=True) 
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True) 
    status = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    confirmed = models.BooleanField(default=False)
    fromStaff = models.ForeignKey(StaffProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='fromStaff')


