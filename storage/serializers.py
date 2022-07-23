from importlib.util import source_hash
from xml.parsers.expat import model
from .models import *
from users.serializers import StaffSerializer
from rest_framework import serializers
import uuid

from django.db.models import Sum

class WarehouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Warehouse
        fields = '__all__'


class TypeAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeAsset
        fields = ["id","name"]

class AssetSerializer(serializers.ModelSerializer):
    typeid =  serializers.SerializerMethodField('get_type')
    

    class Meta:
        model = Asset
        fields = [
            'id', 'sku', 'name', 'quantity',
            'img', 'created_at','updated_at',
            'branch', 'detail', 'type', 'typeid', 'description'
        ]

    def get_type(self, obj):
        if obj.type:
            typeid = TypeAsset.objects.filter(id=obj.type.id).first()
            serializer = TypeAssetSerializer(typeid)
            return serializer.data
        return {} 

    #custom post asset generator sku: format_example(PVS-1234567) 
    def create(self, validated_data):
        post = Asset(**validated_data)
        post.sku = str('PVS-') + str(uuid.uuid4().int)[:7]
        post.save()
        return post

class AssetNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'sku', 'name', 'img']

class AssetDetailSerializer(serializers.ModelSerializer):
    name =  serializers.SerializerMethodField('get_asset_name')
    children = serializers.SerializerMethodField(
        read_only=True, method_name="get_child_categories")
    warehouses = serializers.SerializerMethodField('get_warehouse')
        
    class Meta:
        model = AssetDetail
        fields = [
            'id', 'asset','name', 'serial_no', 'barcode',
            'barcode_img', 'purpose', 'active', 'price', 'ip_source', 'warranty_time',	
            'created_at', 'updated_at', 'warehouse', 'warehouses',
            'dependency', 'children', 'description', 'commerce'
        ]    

    def get_warehouse(self, obj):
        if obj.warehouse:
            warehouse_pk = Warehouse.objects.filter(id=obj.warehouse.id).first()
            serializer = WarehouseSerializer(warehouse_pk)
            return serializer.data
        return {}       
                        
    def get_child_categories(self, obj):
        serializer = AssetDetailSerializer(
            instance=obj.children.all().order_by('asset').distinct(),
            many=True
        )
        return serializer.data     

    def get_asset_name(self, obj):
        asset_name = Asset.objects.filter(id=obj.asset.id).first()
        serializer = AssetNameSerializer(asset_name)
        return serializer.data

    #custom post detail generator barcode
    def create(self, validated_data):
        post = AssetDetail(**validated_data)
        post.barcode = str(uuid.uuid4().int)[:13]
        post.save()
        return post

class TimelineSerializer(serializers.ModelSerializer):
    as_detail_fk = serializers.SerializerMethodField('get_as_detail')
    manager_fk = serializers.SerializerMethodField('get_manager')
    class Meta:
        model = Timeline
        fields = [
            'id', 'detail_asset', 'as_detail_fk',
            'manager', 'manager_fk', 'created_time',
            'updated_time', 'status', 'address', 'confirmed'
        ]


    def get_as_detail(self, obj):
        if obj.detail_asset:
            as_detail = AssetDetail.objects.filter(id=obj.detail_asset.id).first()
            serializer = AssetDetailSerializer(as_detail)
            return serializer.data
        return {}

    def get_manager(self, obj):
        if obj.manager:
            manager = StaffProfile.objects.filter(user=obj.manager.user).first()
            serializer = StaffSerializer(manager)
            return serializer.data
        return {}


