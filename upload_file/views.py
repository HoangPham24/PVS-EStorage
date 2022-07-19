
from contextvars import copy_context
from django.shortcuts import render
from rest_framework.decorators import  api_view
from storage.models import Asset
from storage.serializers import AssetSerializer
from users.models import User, StaffProfile
from users.serializers import StaffSerializer
import codecs
import csv
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage

from django.http import  HttpResponse



# Create your views here.


fs = FileSystemStorage(location='tmp/')
# Viewset


# ------------------Import-Export-Asset---------------

@api_view(['POST'])
def upload_file(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)
        serializer = AssetSerializer(data=data, many=True) 
        status = {}
        if serializer.is_valid():
            serializer.save()    
            product_list = []
            for row in serializer.data:
                product_list.append(
                    Asset(
                        sku=row["sku"],
                        name=row["name"],
                        quantity=row["quantity"],
                        branch=row["branch"],
                        detail=row["detail"],
                        type_id=row["type"],
                        description=row["description"],
                    )
                )
            check = Asset.objects.filter(sku=row['sku']).count()
            if check == 0:
                Asset.objects.bulk_create(product_list)
                
            status["success"] = "Upload file successfull!!"  
            return Response(status)    



@api_view(['GET',])
def export_file(request):
    if request.method == 'GET':
        
        response = HttpResponse(content_type='text/ms-excel')

        writer = csv.writer(response)
        writer.writerow(['id', 'sku', 'name', 'quantity', 'branch', 'detail', 'type', 'description'])
        
        for member in Asset.objects.all().values_list('id', 'sku', 'name', 'quantity', 'branch', 'detail', 'type', 'description'):
            writer.writerow(member)

        response['Content-Disposition'] = 'attachment; filename="asset.csv"'

        return response

# ------------------Import-Export-Users---------------
@api_view(['POST'])
def upload_file_user(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        status = {}
        for row in reader:
            id = row["id"]
            email = row["email"]
            password = row["password"]
            Post=User(is_staff=True, email=email, id=id)
            Post.set_password(password)
            Post.save()
            status["success"] = "Upload file successfull!!"  
        return Response(status) 
        
        

@api_view(['GET',])
def export_file_user(request):
    if request.method == 'GET':
        
        response = HttpResponse(content_type='text/ms-excel')

        writer = csv.writer(response)
        writer.writerow(['id', 'email', 'password', 'is_staff', 'is_active', 'is_admin'])
        
        for member in User.objects.all().values_list('id', 'email', 'password', 'is_staff', 'is_active', 'is_admin'):
            writer.writerow(member)

        response['Content-Disposition'] = 'attachment; filename="users.csv"'

        return response    


# ------------------Import-Export-StaffProfile---------------
@api_view(['POST'])
def upload_file_staff(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)
        serializer = StaffSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            staff_list = []
            
            for row in serializer.data:
                staff_list.append(
                    StaffProfile(
                        user_id=row["user"],
                        name=row["name"],
                        position=row["position"],
                        department=row["department"],
                        joined=row["joined"],
                        contract=row["contract"],
                        phone=row["phone"],
                    )
                )
            check = StaffProfile.objects.filter(user_id=row['user']).count()
            if check == 0:      
                StaffProfile.objects.bulk_create(staff_list)
            
            return Response("success: Upload file successfull!!") 
        return Response("errors: User_id is already exist!!")      

@api_view(['GET',])
def export_file_staff(request):
    if request.method == 'GET':

        response = HttpResponse(content_type='text/ms-excel')

        writer = csv.writer(response)
        writer.writerow(['user', 'name', 'position', 'department', 'joined', 'contract', 'phone'])
        
        for member in StaffProfile.objects.all().values_list('user', 'name', 'position', 'department', 'joined', 'contract', 'phone'):
            writer.writerow(member)

        response['Content-Disposition'] = 'attachment; filename="staffs.csv"'

        return response     