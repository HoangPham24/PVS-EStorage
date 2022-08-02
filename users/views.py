from .models import *
from .serializers import  (UserSerializer, StaffSerializer, DepartmentSerializer, 
                        ChangePasswordSerializer)
from rest_framework.decorators import api_view
from rest_framework import  status, generics
from rest_framework.response import Response 
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated 
from django.db import transaction






# Create your views here.

  

#-------------------Department API --------------------------------
@swagger_auto_schema(tags=["department-api"], methods=['GET'], )
@api_view(['GET',])
def get_department(request):
    if request.method == 'GET':
        department = Department.objects.all()
        serializer = DepartmentSerializer(department, many=True)
        
        response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'GET-DATA-SUCCESS',
                'data': serializer.data
            }

        return Response(response)
        
@swagger_auto_schema(tags=["department-api"], methods=['POST'], request_body=DepartmentSerializer)
@api_view(['POST',])
def post_department(request):
    if request.method == 'POST':
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ------------------End Department API-----------------


#-------------------User API --------------------------------
@swagger_auto_schema(tags=["users-api"], methods=['GET'], )
@api_view(['GET', ])
def get_users(request):
    if request.method == 'GET':
        users = User.objects.filter(is_active=True).order_by('id')
        serializer = UserSerializer(users, many=True)
        response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'GET-DATA-SUCCESS',
                'data': serializer.data
            }

        return Response(response)

@swagger_auto_schema(tags=["users-api"], methods=['POST'], request_body=UserSerializer)
@api_view(['POST',])
def post_users(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(tags=["users-api"], methods=['GET'], )
@api_view(['GET', ])
def get_user_username(request, email=None):
    try:
        users = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)   

    if request.method == 'GET':
        serializer = UserSerializer(users)
        response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'GET-DATA-SUCCESS',
                'data': serializer.data
            }

        return Response(response)

@swagger_auto_schema(tags=["users-api"], methods=['DELETE'], )
@api_view(['DELETE', ])
def delete_user_username(request, username=None):
    try:
        users = User.objects.get(email=username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'DELETE':
        operation = users.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failture"] = "delete failed"    
        return Response(data=data)               
#------------------- End User API --------------------------------



#-------------------Staff API --------------------------------
@swagger_auto_schema(tags=["staff-api"], methods=["GET",])
@api_view(['GET',  ])
def get_staff(request):
    if request.method == 'GET':
        staffs = StaffProfile.objects.all()
        serializer = StaffSerializer(staffs, many=True)
        response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'GET-DATA-SUCCESS',
                'data': serializer.data
            }

        return Response(response)

@swagger_auto_schema(tags=["staff-api"], methods=['post'], request_body=StaffSerializer)
@api_view(['POST'])
def post_staff(request):
    if request.method == 'POST':
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(tags=["staff-api"], methods=["GET",])
@api_view(['GET', ])
def get_staff_pk(request, pk, format=None):
    try:
        staffs = StaffProfile.objects.get(pk=pk)
    except StaffProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)   

    if request.method == 'GET':
        serializer = StaffSerializer(staffs)
        response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'GET-DATA-SUCCESS',
                'data': serializer.data
            }

        return Response(response)

@swagger_auto_schema(tags=["staff-api"], methods=['PUT',], request_body=StaffSerializer)
@api_view(['PUT',])
def update_staff_pk(request, pk, format=None):
    try:
        staffs = StaffProfile.objects.get(pk=pk)
    except StaffProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)   
    if request.method == 'PUT':
        serializer = StaffSerializer(staffs, data=request.data, partial= True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update succesful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(tags=["staff-api"], methods=['DELETE',])
@api_view(['DELETE',])
def delete_staff_pk(request, pk, format=None):
    try:
        staffs = StaffProfile.objects.get(pk=pk)
        user = staffs.user_id  
    except StaffProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)   
    if request.method == 'DELETE':
        with transaction.atomic():
            operation = staffs.delete()
            User.objects.filter(id=user).delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failture"] = "delete failed"    
        return Response(data=data)                  
#-------------------End Staff API --------------------------------


# ----------------Change password -------------------- 

class ChangePasswordView(generics.UpdateAPIView):
    
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': [serializer.data]
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
# ----------------END Change password --------------------

    
                