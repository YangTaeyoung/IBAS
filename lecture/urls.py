from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.lect_register, name="lect_register"),  # lecture 게시판 등록페이지로 이동
    path('detail/<int:lect_no>/', views.lect_detail, name="lect_detail"),  # lecture 게시판 상세보기페이지로 이동
    path('<int:type_no>/view/', views.lect_view, name="lect_view"),  # 강의 리스트 페이지로 이동
    path('aor/<int:lect_no>/', views.lect_aor, name="lect_aor"),  # 강의 등록 거절 페이지
    path('update/<int:lect_no>', views.lect_update, name="lect_update"),
    path('delete/<int:lect_no>', views.lect_delete, name="lect_delete"),
    path('<int:type_no>/search/', views.lect_search, name="lect_search"),
    path('room/main/', views.lectRoom_main, name="lectRoom_main"), # 강의룸 메인 게시판으로 이동
]
