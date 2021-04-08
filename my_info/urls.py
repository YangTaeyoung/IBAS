from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.my_info, name='my_info'),
    path('user/update/register/', views.user_update_request_register, name='user_update_request_register'),
    path('user/update/aor/', views.user_update_request_aor, name="user_update_request_aor"),
    path('user/update/pic/', views.user_pic_update, name="user_pic_update"),
]
