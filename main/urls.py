from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),  # 메인페이지 이동 링크
    path('intro/', views.intro, name="intro"),  # 소개페이지 링크
    path('history/delete/', views.history_delete, name="history_delete"),  # 소개페이지 연혁 삭제
    path('history/register/', views.history_register, name="history_register"),  # 소개페이지 연혁 등록
    path('history/update/', views.history_update, name="history_update"),  # 소개페이지 연혁 수정
    path('test/introduce/', views.test_introduce, name='test_introduce'),  # 동아리 소개 작업
    path('test/test_activity/', views.test_activity, name='test_activity'),  # 동아리 활동 게시판
    path('test/test_activity/detail/', views.test_activity_detail, name='test_activity_detail'),  # 동아리 활동 자세히 보기
    path('test/test_activity/register/', views.test_activity_register, name='test_activity_register'),  # 동아리 등록하기
    path('test/test_activity/delete/', views.test_activity_delete, name='test_activity_delete'),  # 동아리 활동 글 삭제하기
    path('test/test_activity/comment/', views.activity_comment, name='activity_comment'),
    path('test/test_activity_v1/', views.test_activity_v1, name='test_activity_v1'),  # 승연이의 동아리활동 게시판 시도
]
