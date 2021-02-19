from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('join/', views.join, name="join"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('quest/', views.join_chk, name="join_chk"),
    path('join/chk', views.quest_chk, name="quest_chk"),
    path('pass/', views.pass_param, name="pass"),
    path('test/join1/', views.test_join1, name="test_join1"),
    path('test/join2/', views.test_join2, name="test_join2"),
    path('test/std_or_pro/', views.std_or_pro, name="std_or_pro"),
]
