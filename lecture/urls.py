from django.urls import path, include
from . import views

urlpatterns = [
    path('register', views.lecture_register, name="lecture_register"),  # lecture 게시판 등록페이지로 이동
    path('detail', views.lecture_detail, name="lecture_detail")  # lecture 게시판 상세보기페이지로 이동

]