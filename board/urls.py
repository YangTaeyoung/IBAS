from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.board, name="board"), #게시판페이지로 이동
]
