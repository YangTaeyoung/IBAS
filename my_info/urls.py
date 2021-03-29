from django.urls import path, include
from . import views

urlpatterns = [
    path('my_info/', views.my_info, name='my_info')
]