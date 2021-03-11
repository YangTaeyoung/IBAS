from django.urls import path, include
from . import views

# Media files 저장 및 전달 설정하기 위한 import
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('list/', views.bank_board, name='bank_board'),  # 회계 게시판 작업
    path('support/board', views.bank_support_board, name='bank_support_board'),  # 회계 게시판 목록
    path('support/register', views.bank_support_register, name='bank_support_register'),  # 회계 게시판 목록
    path('support/detail', views.bank_support_detail, name='bank_support_detail'),  # 회계 게시판 목록

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
