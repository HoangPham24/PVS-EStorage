from django.contrib import admin
from storage.models import *
from import_export.admin import ImportExportActionModelAdmin


class AssetDetailAdmin(ImportExportActionModelAdmin):
    model = AssetDetail
    list_display = ["asset", "barcode", "price", "dependency", "commerce", "warehouse" ]


class TypeAssetAdmin(ImportExportActionModelAdmin):
    list_display = ["name"]
    model = TypeAsset

class AssetAdmin(ImportExportActionModelAdmin):
    list_display = ["sku", "name","quantity", "detail", "type"]
    search_fields = ["name"]
    model = Asset

class WarehouseAdmin(ImportExportActionModelAdmin):
    list_display = ["name", "address",]
    search_fields = ["name"]
    model = Warehouse   


class TimelineAdmin(ImportExportActionModelAdmin):
    list_display = ["detail_asset","manager", "created_time", "status",  "confirmed"]
    model = Timeline


 

# Register your models here.

admin.site.register(TypeAsset, TypeAssetAdmin) 
admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetDetail, AssetDetailAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Timeline, TimelineAdmin)



 