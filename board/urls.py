from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:board_type_no>/view/', views.board_view, name="board_view"),  # 게시판페이지로 이동
    path('detail/<int:board_no>/', views.board_detail, name="board_detail"),  # 게시판 상세게시판으로 이동
    path('search/', views.board_search, name="board_search"),
    path('register/', views.board_register, name="board_register"),
    path('update', views.board_update, name="board_update"),
    path('delete', views.board_delete, name="board_delete"),
    path('comment/update/', views.board_comment_update, name="board_comment_update"),
    path('comment/delete/', views.board_comment_delete, name="board_comment_delete"),
    path('comment/register/', views.board_comment_register, name="board_comment_register"),

    # 공모전 게시판
    path('contest/list', views.contest_list, name="contest_list"),  # 공모전 게시판페이지로 이동
    path('contest/register', views.contest_register, name="contest_register"),  # 공모전 게시판 등록페이지로 이동
    path('contest/detail/<int:contest_no>', views.contest_detail, name="contest_detail"),  # 공모전 게시판 상세보기페이지로 이동
    path('contest/delete', views.contest_delete, name="contest_delete"),
    path('contest/update', views.contest_update, name="contest_update"),
    path('contest/comment/update', views.contest_comment_update, name="contest_comment_update"),
    path('contest/comment/delete', views.contest_comment_delete, name="contest_comment_delete"),
    path('contest/comment/register', views.contest_comment_register, name="contest_comment_register"),
]
