from django.urls import path, include
from . import views

urlpatterns = [
    path('contest/list', views.contest_list, name="contest_list") # 공모전 게시판페이지로 이동
]
