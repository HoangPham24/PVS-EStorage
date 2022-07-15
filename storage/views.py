import uuid
from django.http import HttpResponse
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework import  status
from rest_framework.response import Response    
from .models import Asset, Timeline, TypeAsset, AssetDetail, Warehouse
from .serializers import *
from django.db import transaction

# Create your views here.


#---------------TypeAsset API-------------
@swagger_auto_schema(tags=["type-asset-api"], method="GET", )
@api_view(['GET', ])
def get_type_api(request):
    
    if request.method == 'GET':
        type = TypeAsset.objects.all()
        serializer = TypeAssetSerializer(type, many=True)
        return Response(serializer.data)     

@swagger_auto_schema(tags=["type-asset-api"], methods=['POST',], request_body=TypeAssetSerializer)
@api_view(['POST',])
def post_tpye_api(request):
    if request.method == 'POST':
        serializer = TypeAssetSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

#-------------END Type Asset API------------



#------------------ Asset API-----------------------
@swagger_auto_schema(tags=["asset-api"], method="GET", )
@api_view(['GET',])
def get_asset(request):
    if request.method == 'GET':
        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)

@swagger_auto_schema(tags=["asset-api"], methods=['POST',], request_body=AssetSerializer)
@api_view(['POST',])
def post_asset(request):
    if request.method == 'POST':
        serializer = AssetSerializer(data=request.data) 
        if serializer.is_valid():
            asset = serializer.save()
            #get quantity asset
            quantity = asset.quantity 
            #auto add detail
            for i in range(quantity):
                AssetDetail.objects.create(
                    asset_id=asset.id, 
                    #generator barcode post asset
                    barcode = str(uuid.uuid4().int)[:13],   
                    
                )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(tags=["asset-api"], method="GET", )
@api_view(['GET', ])
def get_asset_pk(request, pk, format=None):
    try:
        asset_item = Asset.objects.get(pk=pk)
    except Asset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)   

    if request.method == 'GET':
        serializer = AssetSerializer(asset_item)
        return Response(serializer.data)

@swagger_auto_schema(tags=["asset-api"], method="PUT", request_body=AssetSerializer )
@api_view(['PUT', ])
def update_asset_pk(request, pk, format=None):
    try:
        asset_item = Asset.objects.get(pk=pk)
    except Asset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  
    if request.method == 'PUT':
        serializer = AssetSerializer(asset_item, data=request.data, partial= True)
        data = {}

        if serializer.is_valid(): 
            serializer.save()
            data["success"] = "update succesful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@swagger_auto_schema(tags=["asset-api"], method='DELETE',)
@api_view(['DELETE', ])
def delete_asset_pk(request, pk):
    try:
        asset_item = Asset.objects.get(pk=pk)
    except Asset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        operation = asset_item.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failture"] = "delete failed"    
        return Response(data=data)    

# -----------------End Asset API------------------ 



#---------------------Asset Detail API-----------------

@swagger_auto_schema(tags=["asset-detail-api"], method="GET", )
@api_view(['GET', ])
def get_asset_detail(request):
    if request.method == 'GET':
        detail_asset = AssetDetail.objects.all().order_by('asset').distinct()
        serializer = AssetDetailSerializer(detail_asset, many=True)
        return Response(serializer.data)

@swagger_auto_schema(tags=["asset-detail-api"], methods=['POST',], request_body=AssetDetailSerializer)
@api_view(['POST', ])
def post_asset_detail(request):
    if request.method == 'POST':
        serializer = AssetDetailSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            asset = Asset.objects.get(id=request.data['asset'])
            count = AssetDetail.objects.filter(asset_id=asset.id).count()
            with transaction.atomic():
                Asset.objects.filter(id=request.data['asset']).update(quantity=count)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(tags=["asset-detail-api"], method="GET", )
@api_view(['GET', ])
def get_asset_detail_pk(request, id_asset, format=None):
    try:
        asset_detail = AssetDetail.objects.filter(asset__pk=id_asset)
    except AssetDetail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  
        
    if request.method == 'GET':
        serializer = AssetDetailSerializer(asset_detail, many=True)
        return Response(serializer.data)


@swagger_auto_schema(tags=["asset-detail-api"], method='DELETE',)
@api_view(['DELETE', ])
def delete_asset_detail_pk(request, id_asset):
    try:
        asset_detail = AssetDetail.objects.filter(asset__pk=id_asset)
    except AssetDetail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  
    if request.method == 'DELETE':
        asset = Asset.objects.get(id=id_asset)
        with transaction.atomic():
            operation = asset_detail.delete()
            count = AssetDetail.objects.filter(asset_id=asset.id).count() 
            Asset.objects.filter(id=id_asset).update(quantity=count)
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failture"] = "delete failed"    
        return Response(data=data)      

@swagger_auto_schema(tags=["asset-detail-api"], method="GET", )
@api_view(['GET', ])
def get_list_children(request, pk, format=None):
    try:
        asset_detail = AssetDetail.objects.filter(pk=pk)
    except AssetDetail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  
        
    if request.method == 'GET':
        serializer = AssetDetailSerializer(asset_detail, many=True)
        return Response(serializer.data)

@swagger_auto_schema(tags=["asset-detail-api"], method="GET", )
@api_view(['GET', ])
def get_barcode(request, barcode, format=None):
    try:
        barcode__pk = AssetDetail.objects.filter(barcode=barcode)
    except AssetDetail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  
        
    if request.method == 'GET':
        serializer = AssetDetailSerializer(barcode__pk, many=True)
        return Response(serializer.data)

@swagger_auto_schema(tags=["asset-detail-api"], methods=['PUT',], request_body=AssetDetailSerializer)
@api_view(['PUT', ])
def update_asset_detail(request, pk, format=None):
    try:
        asset_detail = AssetDetail.objects.get(pk=pk)
    except AssetDetail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)   

    if request.method == 'PUT':
        serializer = AssetDetailSerializer(asset_detail, data=request.data, partial = True)
        data = {}
        if serializer.is_valid(): 
            serializer.save()
            data["success"] = "update succesful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@swagger_auto_schema(tags=["asset-detail-api"], method='DELETE',)
@api_view(['Delete', ])
def delete_asset_detail(request, pk):
    try:
        asset_detail = AssetDetail.objects.get(pk=pk)
        asset = asset_detail.asset
    except AssetDetail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  
    if request.method == 'DELETE':
        with transaction.atomic():
            operation = asset_detail.delete()
            count = AssetDetail.objects.filter(asset_id=asset.id).count() 
            asset.quantity = count
            asset.save()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failture"] = "delete failed"    
        return Response(data=data)        

# -------------------END Asset Detail API----------------


#---------------------Timeline API-----------------
@swagger_auto_schema(tags=["timeline-api"],methods=['GET'], )
@api_view(['GET', ])
def get_timeline(request):
    if request.method == 'GET':
        timelines = Timeline.objects.all().order_by('detail_asset', 'created_time').distinct()
        serializer = TimelineSerializer(timelines, many=True)
        return Response(serializer.data)

@swagger_auto_schema(tags=["timeline-api"], methods=['POST'], request_body=TimelineSerializer)
@api_view(['POST', ])
def post_timeline(request):
    if request.method == 'POST':
        serializer = TimelineSerializer(data=request.data, many=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

@swagger_auto_schema(tags=["timeline-api"], methods=['GET'],)
@api_view(['GET', ])
def get_timeline_pk(request, id_detail_asset, format=None):
    try:
        timeline_item = Timeline.objects.filter(detail_asset__pk=id_detail_asset)
    except Timeline.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  
        
    if request.method == 'GET':
        serializer = TimelineSerializer(timeline_item, many=True)
        return Response(serializer.data)                  


@swagger_auto_schema(tags=["timeline-api"], methods=['PUT'], request_body=TimelineSerializer)
@api_view(['PUT', ])
def update_timeline(request, pk, format=None):
    try:
        timeline_item = Timeline.objects.get(pk=pk)
    except Timeline.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = TimelineSerializer(timeline_item, data=request.data, partial = True)
        data = {}
        if serializer.is_valid():
            serializer.save() 
            data["success"] = "update succesful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@swagger_auto_schema(tags=["timeline-api"], methods=['DELETE'],)
@api_view(['DELETE', ])
def delete_timeline(request, pk, format=None):
    try:
        timeline_item = Timeline.objects.get(pk=pk)
    except Timeline.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        operation = timeline_item.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failture"] = "delete failed"    
        return Response(data=data)     

@swagger_auto_schema(tags=["timeline-api"], method="GET", )  
@api_view(['GET', ])   
def timeline_pk_manager(request, id_manager, format=None):
    try:
        manager = Timeline.objects.filter(manager__pk=id_manager)
    except Timeline.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  
        
    if request.method == 'GET':
        serializer = TimelineSerializer(manager, many=True)
        return Response(serializer.data) 

@swagger_auto_schema(tags=["timeline-api"], method="GET", )  
@api_view(['GET', ])   
def get_confirmed(request, id_manager):
    try:
        manager = Timeline.objects.filter(manager__pk=id_manager, confirmed=False)
    except Timeline.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  
        
    if request.method == 'GET':
        serializer = TimelineSerializer(manager, many=True)
        return Response(serializer.data) 

@swagger_auto_schema(tags=["timeline-api"], method="GET", )  
@api_view(['GET',])
def get_lasted_timeline(request, id_asdetail, format=None):
    try:
        timeline_item = Timeline.objects.filter(
            detail_asset__pk=id_asdetail
        ).order_by('-created_time')[:2]
    except Timeline.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  
        
    if request.method == 'GET':
        serializer = TimelineSerializer(timeline_item, many=True)
        return Response(serializer.data) 

# -----------------End Timeline API------------------ 


# --------------------Warehouse API------------------------
@swagger_auto_schema(tags=["warehouse-api"], method="GET", )
@api_view(['GET',])
def get_warehouse(request):
    if request.method == 'GET':
        timelines = Warehouse.objects.all()
        serializer = WarehouseSerializer(timelines, many=True)
        return Response(serializer.data)

@swagger_auto_schema(tags=["warehouse-api"], method="POST", request_body=WarehouseSerializer)        
@api_view(['POST',])
def post_warehouse(request):
    if request.method == 'POST':
        serializer = WarehouseSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(methods=['put'], request_body=WarehouseSerializer)
@api_view(['PUT', 'DELETE' ])
def warehouse_pk(request, pk, format=None):
    try:
        warehouse = Warehouse.objects.get(pk=pk)
    except Warehouse.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = WarehouseSerializer(warehouse, data=request.data, partial = True)
        data = {}
        if serializer.is_valid():
            serializer.save() 
            data["success"] = "update succesful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE':
        operation = warehouse.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failture"] = "delete failed"    
        return Response(data=data)
# --------------------END Warehouse API------------------------

