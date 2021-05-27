from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.my_info, name='my_info'),
    path('user/update/register/', views.user_update_request_register,
         name='user_update_request_register'),
    path('user/update/aor/', views.user_update_request_aor, name="user_update_request_aor"),
    path('user/update/pic/', views.user_pic_update, name="user_pic_update"),
    path('user/update/major/', views.user_major_update, name="user_major_update"),
    path('user/update/phone/', views.user_phone_update, name="user_phone_update"),
    path('user/delete/pic/', views.user_pic_delete, name="user_pic_delete"),
]
