from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.my_info, name='my_info'),
    path('user/activate/request/', views.user_activate_request, name='user_activate_request'),
    path('user/update/register/', views.user_update_request_register,
         name='user_update_request_register'),
    path('user/update/aor/', views.user_update_request_aor, name="user_update_request_aor"),
    path('user/update/pic/', views.user_pic_update, name="user_pic_update"),
    path('user/update/intro/', views.user_intro_update, name="user_intro_update"),
    path('user/update/major/', views.user_major_update, name="user_major_update"),
    path('user/update/phone/', views.user_phone_update, name="user_phone_update"),
    path('user/update/grade/', views.user_grade_update, name="user_grade_update"),
    path('user/delete/pic/', views.user_pic_delete, name="user_pic_delete"),
    path("user/withdrawal/", views.withdrawal, name="user_withdrawal"),
    path('connnect/social/account/', views.connect_social_account, name="connect_social_account"),
    path("connnect/social/account/before/set/", views.go_social_login_before_setting,
         name="connect_social_account_before_setting"),

]
