
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/', include('allauth.urls')),
    path('pass/', views.loginchk, name="loginchk")
]

