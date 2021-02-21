
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('main1/', views.index1, name='index1'),
    path('main2/', views.index2, name='index2'),
    path('accounts/', include('allauth.urls')),
]

