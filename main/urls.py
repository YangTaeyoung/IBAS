
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('main1/', views.index1, name='index1'), # 탑바 작업
    path('main2/', views.index2, name='index2'), # 메인 작업
    path('main3/', views.index3, name='index3'), # 동아리 소개 작업
    path('accounts/', include('allauth.urls')),
]

