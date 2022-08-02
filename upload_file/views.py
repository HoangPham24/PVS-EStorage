from rest_framework.decorators import  api_view
from storage.models import Asset, AssetDetail, Timeline
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from rest_framework import  status
from django.http import  HttpResponse
from .serializers import GetApiSerializer, GetCreated
from drf_yasg.utils import swagger_auto_schema
from .models import *
import uuid
from tablib import Dataset
from django.views.decorators.csrf import csrf_exempt
import io
import xlsxwriter

# Create your views here.


fs = FileSystemStorage(location='tmp/')
# Viewset
@swagger_auto_schema(tags=["GET-API-PVS"], method="GET")
@api_view(['GET',])
def get_asset_pvs_api(request):
    if request.method == 'GET':
        getapi = GetApiPVS.objects.all().order_by('id')
        serializer = GetApiSerializer(getapi, many=True)
        
        return Response(serializer.data)

@swagger_auto_schema(tags=["GET-API-PVS"], method="POST", request_body=GetCreated)
@api_view(['POST',])
def post_pvs_asset_api(request):
    if request.method == 'POST':
        serializer = GetCreated(data=request.data) 
        if serializer.is_valid():
            api = serializer.save()
            ct = api.content
            creator = api.creator
            for i in ct.split('\n'):
                k = i.split(';')
                asset = Asset.objects.create(
                    sku = str('PVS-') + str(uuid.uuid4().int)[:7],
                    name = k[1],
                    quantity = int(k[2]),
                )   
                quantity = asset.quantity
                for s in range(quantity):
                    detail = AssetDetail.objects.create(
                        asset_id = asset.id,
                        barcode = str(uuid.uuid4().int)[:13], 
                        price = k[3]
                    ) 
                for t in range(quantity):
                    Timeline.objects.create(
                        detail_asset_id= detail.id,
                        manager_id=creator.id,
                        confirmed=True,
                        fromStaff_id=creator.id
                    )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

@swagger_auto_schema(tags=["GET-API-PVS"], method="PUT", request_body=GetCreated)
@api_view(['PUT',])
def update_pvs_asset_api(request, pk):
    try:
        asset = GetApiPVS.objects.get(pk=pk)
    except GetApiPVS.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = GetCreated(asset, data=request.data, partial = True)
        data = {}
        if serializer.is_valid():
            serializer.save() 
            data["success"] = "Update succesful"
            return Response(data)   
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  



# ------------------Import-Export-Asset---------------

@api_view(['POST',])
@csrf_exempt 
def upload_file_asset(request):
    status = {}
    if request.method == "POST":
        dataset = Dataset()
        file = request.FILES['file']

        imported_data = dataset.load(file.read(),format='xlsx')
        #print(imported_data)
        for data in imported_data:
                name = data[0]
                quantity = data[1]
                commerce = data[2]
                branch = data[3]
                detail = data[4]
                price = data[5]
                data = {}
                
                post = Asset(
                    sku = str('PVS-') + str(uuid.uuid4().int)[:7],
                    name = name, quantity = quantity, branch = branch, 
                    detail = detail
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
                        commerce = False
                    )
                if commerce is not None:
                    for i in range(commerce):
                        AssetDetail.objects.create(
                            asset_id=asset.id,
                            barcode = str(uuid.uuid4().int)[:13],
                            price = price,
                            commerce = True
                        )
            
                total = AssetDetail.objects.filter(asset_id=asset.id).count()
                print (total)
                asset.quantity = total 
                asset.save()
        status["success"] = "Upload file successfull!!"  
    return Response(status)
                      

def get_simple_table_data():
    # Simulate a more complex table read.
    return [['Tên tài sản', 'Số lượng tài sản nội bộ', 'Số lượng tài sản thương mại',
             'Ngành hàng', 'Mô tả chi tiết ', 'Giá trị tài sản']]

@api_view(['GET',])
def download(request):
 
    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    data = get_simple_table_data()

    # Write some test data.
    for row_num, columns in enumerate(data):
        for col_num, cell_data in enumerate(columns):
            worksheet.write(row_num, col_num, cell_data)

    # Close the workbook before sending the data.
    workbook.close()

    # Rewind the buffer.
    output.seek(0)
    
    # Set up the Http response.
    filename = 'asset.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


