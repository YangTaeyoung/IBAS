
from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('join/', views.join, name="join"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('join.do/', views.join_chk, name="join_chk"),
    path('pass/', views.pass_param, name="pass"),
    path('test/join', views.test_join, name="test_join")
]