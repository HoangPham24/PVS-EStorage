from django.urls import path, include
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView )
from . import views 
from .views import ChangePasswordView





urlpatterns = [
    path('api/upload-users-xlsx', views.user_upload, name='user_upload'),
    path('api/change-password', ChangePasswordView.as_view(), name='change-password'),
    #User uls
    path('api/get-users/', views.get_users),
    path('api/post-users', views.post_users),
    path('api/users-pk/<str:username>', views.get_user_username),
    path('api/delete-username/<str:email>', views.delete_user_username),
    #Staff uls
    path('api/get-staffprofile', views.get_staff),
    path('api/post-staffprofile', views.post_staff),
    path('api/get-staffprofile-pk/<int:pk>', views.get_staff_pk),
    path('api/update-staffprofile-pk/<int:pk>', views.update_staff_pk),
    path('api/delete-staffprofile-pk/<int:pk>', views.delete_staff_pk),
    #Department uls
    path('api/get-department', views.get_department),
    path('api/post-department', views.post_department),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #API PVS
    path('get-staff-api-PVS/', views.get_staff_pvs),
    path('get-users-api-PVS/', views.get_users_pvs),
]

