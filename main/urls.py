
from django.urls import path, include
from . import views

urlpatterns = [
    path('main', views.main, name="main"), #메인
    path('main/top_bar/', views.top_bar, name='top_bar'), # 탑바 작업
    path('main/bottom_bar', views.bottom_bar, name='bottom_bar'), # 하단 바 작업
    path('main/test_activity/', views.test_activity, name='test_activity'), # 동아리 소개 작업
    path('accounts/', include('allauth.urls')),
]

