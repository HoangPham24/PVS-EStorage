from django.urls import path
from . import views


urlpatterns = [
    #TypeAsset urls
    path('api/get-type-asset', views.get_type_api),
    path('api/post-type-asset', views.post_tpye_api),
    #Asset urls
    path('api/get-asset', views.get_asset),
    path('api/post-asset', views.post_asset),
    path('api/get-asset-pk/<int:pk>', views.get_asset_pk),
    path('api/update-asset-pk/<int:pk>', views.update_asset_pk),
    path('api/delete-asset-pk/<int:pk>', views.delete_asset_pk),
    #AssetDetail urls
    path('api/get-asset-detail', views.get_asset_detail),
    path('api/post-asset-detail', views.post_asset_detail),
    path('api/get-asset-detail-pk/<int:id_asset>', views.get_asset_detail_pk),
    path('api/delete-asset-detail-pk/<int:id_asset>', views.delete_asset_detail_pk),
    path('api/update-asset-detail/<int:pk>', views.update_asset_detail),
    path('api/delete-asset-detail/<int:pk>', views.delete_asset_detail),
    path('api/get-list-children/<int:pk>', views.get_list_children),
    path('api/get-barcode/<int:barcode>',views.get_barcode),
    #Timeline urls
    path('api/get-timeline', views.get_timeline),
    path('api/post-timeline', views.post_timeline),
    path('api/timeline-pk-asset/<int:id_detail_asset>', views.get_timeline_pk),
    path('api/update-timeline/<int:pk>', views.update_timeline),
    path('api/delete-timeline/<int:pk>', views.delete_timeline),
    path('api/timeline-pk-manager/<int:id_manager>', views.timeline_pk_manager),
    path('api/confirmed-timeline/<int:id_manager>', views.get_confirmed),
    path('api/timeline_lastest/<int:id_asdetail>', views.get_lasted_timeline),
    #Warehouse urls
    path('api/warehouse', views.get_warehouse),
    path('api/post_warehouse', views.post_warehouse),
   
    

]