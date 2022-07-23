from xml.parsers.expat import model
from .models import *
from rest_framework import serializers
from users.serializers import UserIDSerializer

class GetApiSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField('get_user')
    class Meta:
        model = GetApi
        fields = ['id', 'get_id', 'value', 'content',  'created_by']

    def get_user(self, obj):
        if obj.created_by:
            userid = User.objects.filter(id=obj.created_by.id).first()
            serializer = UserIDSerializer(userid)
            return serializer.data
        return {} 

class GetCreated(serializers.ModelSerializer):
    class Meta:
        model = GetApi
        fields = '__all__'