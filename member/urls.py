
from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('join/', views.join, name="join"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('join.do/', views.join_chk, name="join_chk"),
    path('pass/', views.pass_param, name="pass"),
    path('test/join2/', views.test_join2, name="test_join2"),
]
