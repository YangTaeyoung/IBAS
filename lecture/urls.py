from django.urls import path, include
from . import views

urlpatterns = [
    path('contest/list', views.contest_list, name="contest_list"),# 공모전 게시판페이지로 이동
    path('contest/register', views.contest_register, name="contest_register"), # 공모전 게시판 등록페이지로 이동
    path('contest/detail', views.contest_detail, name="contest_detail") # 공모전 게시판 상세보기페이지로 이동

]
