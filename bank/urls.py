from django.urls import path, include
from . import views

# Media files 저장 및 전달 설정하기 위한 import
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('list/', views.bank_list, name='bank_list'),  # 회계 게시판 작업

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
