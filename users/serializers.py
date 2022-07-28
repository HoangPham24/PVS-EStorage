from rest_framework import serializers
from .models import *



class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "is_active", "is_admin", "is_staff"]

class UserIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]    
        
class StaffNameSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')
    class Meta:
        model = StaffProfile
        fields = ["user", "name", "position"]

    def get_user(self, obj):
        if obj.user:
            users = User.objects.filter(id=obj.user.id).first()
            serializer = UserIDSerializer(users)
            return serializer.data
        return {}     
class StaffSerializer(serializers.ModelSerializer):
    departmentid = serializers.SerializerMethodField('get_department')
    user_id = serializers.SerializerMethodField('get_user')
    class Meta:
        model = StaffProfile
        fields = [
            "user", "user_id", "name","department", 
            "departmentid","joined","contract","position","phone"
        ]      

    def get_department(self, obj):
        if obj.department:
            department_pk = Department.objects.filter(id=obj.department.id).first()
            serializer = DepartmentSerializer(department_pk)
            return serializer.data
        return {}

    def get_user(self, obj):
        if obj.user:
            users = User.objects.filter(id=obj.user.id).first()
            serializer = UserIDSerializer(users)
            return serializer.data
        return {}    

class ChangePasswordSerializer(serializers.Serializer):
    class Meta:
        model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

       

