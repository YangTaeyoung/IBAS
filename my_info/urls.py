from django.urls import path, include
from . import views

urlpatterns = [
    path('my_info_top/', views.my_info_top, name='my_info_top')
]