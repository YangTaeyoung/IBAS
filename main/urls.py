from django.urls import path, include
from . import views

# Media files 저장 및 전달 설정하기 위한 import
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),  # 메인페이지 이동 링크
    path('test/introduce/', views.test_introduce, name='test_introduce'),  # 동아리 소개 작업
    path('test/test_activity/', views.test_activity, name='test_activity'),  # 동아리 활동 게시판
    path('test/test_activity/detail/', views.test_activity_detail, name='test_activity_detail'),  # 동아리 활동 자세히 보기
    path('test/test_activity/register/', views.test_activity_register, name='test_activity_register'),  # 동아리 등록하기
    path('test/test_activity/delete/', views.test_activity_delete, name='test_activity_delete'), # 동아리 활동 글 삭제하기
    path('test/test_activity/comment/', views.activity_comment, name='activity_comment'), # 동아리 댓글 쓰는 것
    path('test/test_activity/comment/delete', views.activity_comment_delete, name='activity_comment_delete'), # 동아리 댓글 삭제하는 것
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)