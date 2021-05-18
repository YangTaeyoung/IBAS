from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.lect_register, name="lect_register"),  # lecture 게시판 등록페이지로 이동
    path('detail/<int:lect_no>', views.lect_detail, name="lect_detail"),  # lecture 게시판 상세보기페이지로 이동
    path('<int:type_no>/view/', views.lect_view, name="lect_view"),  # 공모전 게시판페이지로 이동
    path('room/main/', views.lectRoom_main, name="lectRoom_main"), # 강의룸 메인 게시판으로 이동
    path('room/register/', views.lect_room_register, name="lect_room_register"), # 강의룸 게시글 등록페이지로 이동
]
