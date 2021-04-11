from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:board_type_no>/view/', views.board_view, name="board_view"),  # 게시판페이지로 이동
    path('detail/<int:board_no>/', views.board_detail, name="board_detail"),  # 게시판 상세게시판으로 이동
    path('search/', views.board_search, name="board_search"),
    path('register/', views.board_register, name="board_register"),
    path('update', views.board_update, name="board_update"),
    path('delete', views.board_delete, name="board_delete"),
    path('contest/list', views.contest_board, name="contest_list"),  # 공모전 게시판페이지로 이동
    path('contest/register', views.contest_register, name="contest_register"),  # 공모전 게시판 등록페이지로 이동
    path('contest/detail', views.contest_detail, name="contest_detail")  # 공모전 게시판 상세보기페이지로 이동

]
