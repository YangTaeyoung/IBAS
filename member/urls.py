from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('allauth.urls')), # 소셜 로그인 관련 링크
    path('join/sop/', views.choose_std_or_pro, name="choose_std_or_pro"), # 학생, 교수 선택 페이지 이동 링크
    path('join/', views.join, name="join"), # 조인 페이지 이동 링크
    path('login/', views.login, name="login"), # 로그인 페이지 이동 링크
    path('logout/', views.logout, name="logout"), # 로그아웃 링크
    path('quest/', views.join_chk, name="join_chk"), # 회원가입 확인 페이지
    path('join/chk', views.quest_chk, name="quest_chk"), # 질문 답변 확인 페이지 랑크
    path('pass/', views.pass_param, name="pass"), # 소셜 로그인으로 부터 받은 정보를 회원가입 페이지로 전송시키는 페이지 (노출X)
    path('welcome/', views.welcome, name="welcome"), # 회원가입 완료 페이지 이동 링크
    path('rulebook/<type_no>', views.rulebook, name="rulebook"),  # 동아리 회칙 / 개인정보 이용동의 페이지 이동 링크
]
