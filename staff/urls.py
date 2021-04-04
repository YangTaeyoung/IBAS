from django.urls import path, include
from . import views

# Media files 저장 및 전달 설정하기 위한 import
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("member/list/", views.staff_member_list, name="staff_member_list"),
    path("member/update/", views.staff_member_update, name="staff_member_update"),
    path('delete/list/', views.member_delete_list, name='member_delete_list'),
    path('delete/detail/', views.member_delete_detail, name='member_delete_detail'),
    path('delete/register/', views.member_delete_register, name='member_delete_register'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)