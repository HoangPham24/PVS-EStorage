from django.urls import path, include
from . import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('upload-file-asset', views.upload_file_asset),
    path('download-form-upload', views.download),
    path('get-asset-api-pvs', views.get_asset_pvs_api),
    path('post-asset-api-pvs', views.post_pvs_asset_api),
    
]

