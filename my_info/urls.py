from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.my_info, name='my_info'),
    path('my_post/', views.my_info, name="my_post"),
]
