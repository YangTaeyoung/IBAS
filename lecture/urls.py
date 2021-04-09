from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.lect_list, name="lect_list") # 공모전 게시판페이지로 이동
]
