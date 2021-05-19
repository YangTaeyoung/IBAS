from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.lect_register, name="lect_register"),  # lecture 게시판 등록페이지로 이동
    path('detail/<int:lect_no>', views.lect_detail, name="lect_detail"),  # lecture 게시판 상세보기페이지로 이동
    path('<int:type_no>/view/', views.lect_view, name="lect_view"), # 공모전 게시판페이지로 이동
    path('room/mem/manage', views.lect_room_mem_manage, name="lect_room_mem_manage"),
    path('room/attend/std', views.lect_room_attend_std, name="lect_room_attend_std"),
    path('room/attend/teacher', views.lect_room_attend_teacher, name="lect_room_attend_teacher")
]
