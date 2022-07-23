from django.urls import path, include
from . import views


urlpatterns = [
  
    path('upload-file-asset', views.upload_file_asset),
    path('export-file-asset', views.export_file),
    path('export-file-user', views.export_file_user),
    path('upload-file-staff', views.upload_file_staff),
    path('get-asset-api-pvs', views.get_asset_pvs_api),
    path('post-asset-api-pvs', views.post_pvs_asset_api),
]