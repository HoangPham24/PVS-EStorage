from django.urls import path, include
from . import views


urlpatterns = [
  
    path('upload-file', views.upload_file),
    path('export-file', views.export_file),
    path('export-file-user', views.export_file_user),
    path('export-file-staff', views.export_file_staff),
    path('upload-file-user', views.upload_file_user),
    path('upload-file-staff', views.upload_file_staff),
]