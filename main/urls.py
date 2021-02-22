from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),  # 메인페이지 이동 링크
]
