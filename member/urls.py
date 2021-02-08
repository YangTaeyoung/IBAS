
from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('join/', views.join, name="join"),
    path('login/', views.login, name="login"),
    path('join.do/', views.join_chk, name="join_chk")

]

