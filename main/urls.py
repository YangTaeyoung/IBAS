from django.urls import path, include
from . import views

# Media files 저장 및 전달 설정하기 위한 import
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),  # 메인페이지 이동 링크
    path('introduce/', views.introduce, name='introduce'),  # 동아리 소개 작업
    path('activity/', views.activity, name='activity'),  # 동아리 활동 게시판
    path('activity/detail/', views.activity_detail, name='activity_detail'),  # 동아리 활동 자세히 보기
    path('activity/register/', views.activity_register, name='activity_register'),  # 동아리 등록하기
    path('activity/update/', views.activity_update, name='activity_update'),  # 동아리 글 수정하기
    path('activity/delete/', views.activity_delete, name='activity_delete'),  # 동아리 활동 글 삭제하기
    path('activity/comment/', views.activity_comment, name='activity_comment'),  # 동아리 댓글 쓰는 것
    path('activity/detail_v1/', views.activity_detail_v1, name='activity_detail_vi'),  # 동아리활동 자세히보기 꾸민ver
    path('activity/comment/delete/', views.activity_comment_delete, name='activity_comment_delete'),  # 동아리 댓글 삭제하는 것
    path('activity/comment/update/', views.activity_comment_update, name='activity_comment_update'),  # 동아리 댓글 수정하는 것

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
