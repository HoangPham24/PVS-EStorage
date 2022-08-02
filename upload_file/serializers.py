from xml.parsers.expat import model
from .models import *
from rest_framework import serializers
from users.serializers import UserIDSerializer

class GetApiSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField('get_user')
    class Meta:
        model = GetApiPVS
        fields = ['id', 'content', 'creator']

    def get_user(self, obj):
        if obj.creator:
            userid = User.objects.filter(id=obj.creator.id).first()
            serializer = UserIDSerializer(userid)
            return serializer.data
        return {} 

class GetCreated(serializers.ModelSerializer):
    class Meta:
        model = GetApiPVS
        fields = '__all__'
