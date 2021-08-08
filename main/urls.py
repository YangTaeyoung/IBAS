from django.urls import path, include
from . import views

# Media files 저장 및 전달 설정하기 위한 import
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="index"),  # 메인페이지 이동 링크
    path('introduce/', views.introduce, name='introduce'),  # 동아리 소개 작업
    path('activity/', views.activity_list, name='activity'),  # 동아리 활동 게시판
    path('activity/<int:board_no>/detail/', views.activity_detail, name='activity_detail'),  # 동아리 활동 자세히 보기
    path('activity/register/', views.activity_register, name='activity_register'),  # 동아리 등록하기
    path('activity/update/<int:board_no>/', views.activity_update, name='activity_update'),  # 동아리 글 수정하기
    path('activity/delete/<int:board_no>/', views.activity_delete, name='activity_delete'),  # 동아리 활동 글 삭제하기
    path('history/register/', views.history_register, name='history_register'),
    path('history/update/', views.history_update, name='history_update'),
    path('history/delete/', views.history_delete, name='history_delete'),
    path('alarm/chk/<int:alarm_no>/', views.alarm_check, name="alarm_check"),
    path('hof/', views.hall_of_fame, name="hall_of_fame"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
