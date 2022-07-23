
from django.shortcuts import render
from rest_framework.decorators import  api_view
from storage.models import Asset, AssetDetail
from users.models import User, StaffProfile
import codecs
import csv
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from rest_framework import  status
from django.http import  HttpResponse
from .serializers import GetApiSerializer, GetCreated
from drf_yasg.utils import swagger_auto_schema
from .models import *
import uuid


# Create your views here.


fs = FileSystemStorage(location='tmp/')
# Viewset
@swagger_auto_schema(tags=["GET-API-PVS"], method="GET")
@api_view(['GET',])
def get_asset_pvs_api(request):
    if request.method == 'GET':
        getapi = GetApi.objects.all()
        serializer = GetApiSerializer(getapi, many=True)
        
        response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'GET-DATA-SUCCESS',
                'data': serializer.data
            }

        return Response(response)

@swagger_auto_schema(tags=["GET-API-PVS"], method="POST", request_body=GetCreated)
@api_view(['POST',])
def post_pvs_asset_api(request):

    if request.method == 'POST':
        serializer = GetCreated(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  





# ------------------Import-Export-Asset---------------

@api_view(['POST'])
def upload_file_asset(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=";")
        status = {}
        for row in reader:
            name = row["name"]
            quantity = row["quantity"]
            branch= row["branch"]
            detail= row["detail"]
            type_id= row["type"]
            description= row["description"]
            price= row["price"]
            check = Asset.objects.filter(name=name).count()
            # print (check)
            data = {}
            if not (name):
                data["error"] = "Name cannot be empty!!"
                return Response(data)
            if check == 0:
                post=Asset(
                    sku=str('PVS-') + str(uuid.uuid4().int)[:7], 
                    name=name, quantity=quantity, branch=branch, detail=detail, 
                    type_id=type_id, description=description
                )
                post.save()
                asset = Asset.objects.get(id=post.id)
                quantity = asset.quantity
                # print (quantity)
                for i in range(quantity):
                    AssetDetail.objects.create(
                        asset_id=asset.id,
                        barcode = str(uuid.uuid4().int)[:13],
                        price = price,
                    )
                   
            elif check != 0:
                try:
                    obj = Asset.objects.get(name=name)
                    obj.quantity = quantity
                    obj.branch = branch
                    obj.detail = detail
                    obj.type_id = type_id
                    obj.description = description
                    obj.save()
                except Asset.DoesNotExist:  
                    Asset.objects.create(
                        quantity=quantity, branch=branch,
                        detail=detail, type_id=type_id, description=description,
                    )
                asset = Asset.objects.get(id=obj.id)
                print (asset)
                sum_quantity = asset.quantity
                # print (quantity)
                for i in range(sum_quantity):
                    # print (i)
                    AssetDetail.objects.create(
                        asset_id=asset.id,
                        barcode = str(uuid.uuid4().int)[:13],
                        price = price,
                    )
                    count = AssetDetail.objects.filter(asset_id=asset.id).count()
                    print (count)
                    asset.quantity = count 
                    asset.save()
            status["success"] = "Upload file successfull!!"  
        return Response(status)       



@api_view(['GET',])
def export_file(request):
    if request.method == 'GET':
        fields = [
            'id',
            'name',
            'quantity',
            'assetdetail__price',
        ]
        print (fields)
        # Generate the csv file with datetime

        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="assets.csv"'
        writer = csv.writer(response)

        # Write the header row
        writer.writerow(['id', 'name', 'quantity', 'price'])
        
        # Use the fields to get the data, specifying the model name
        for row in Asset.objects.values(*fields):
            writer.writerow([row[field] for field in fields])
        # return
        return response 

# ------------------Import-Export-Users---------------
@api_view(['POST'])
def upload_file_staff(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=";")
        status = {}
        for row in reader:
            email = row["email"]
            password = row["password"]
            name = row["name"]
            position = row["position"]
            check = User.objects.filter(email=email).count()
            # print(check)
            data = {}
            if not (email and password):
                data["error"] = "Email and Password cannot be empty!!"
                return Response(data)  
            if check == 0:
                Post=User(is_staff=True, email=email)
                Post.set_password(password)
                Post.save()
                users = User.objects.get(id=Post.id)
                id = users.id
                # print (id)
                for i in str(id):
                    checkst = StaffProfile.objects.filter(user_id=id).count()
                    if checkst == 0:
                        StaffProfile.objects.create(
                            user_id=users.id,
                            name = name,
                            position=position,
                        )
            elif check != 0:
                try:
                    obj = User.objects.get(email=email)
                    obj.set_password(password)
                    obj.save()
                except User.DoesNotExist:  
                    User.objects.create(password=password)
                users = User.objects.get(id=obj.id)
                id = users.id   
                for i in str(id): 
                    checkst = StaffProfile.objects.get(user_id=id)
                    checkst.name = name
                    checkst.position = position
                    checkst.save()
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
      
