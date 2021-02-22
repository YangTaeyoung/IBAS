
from django.urls import path, include
from . import views

urlpatterns = [
    path('test/', views.test_main, name="main"), #메인
    path('test/top_bar/', views.test_top_bar, name='top_bar'), # 탑바 작업
    path('test/bottom_bar/', views.test_bottom_bar, name='test_bottom_bar'), # 하단 바 작업
    path('test/introduce/', views.test_introduce, name='test_introduce'), # 동아리 소개 작업
    path('test/test_activity/', views.test_activity, name='test_activity'), # 동아리 활동 게시판
    path('test/accounts/', include('allauth.urls')),
]

