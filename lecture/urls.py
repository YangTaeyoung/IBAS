from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('register/', views.lect_register, name="lect_register"),  # lecture 게시판 등록페이지로 이동
    path('detail/<int:lect_no>/', views.lect_detail, name="lect_detail"),  # lecture 게시판 상세보기페이지로 이동
    path('<int:type_no>/view/', views.lect_view, name="lect_view"),  # 강의 리스트 페이지로 이동
    path('aor/<int:lect_no>/', views.lect_aor, name="lect_aor"),  # 강의 등록 거절 페이지
    path('update/<int:lect_no>', views.lect_update, name="lect_update"),
    path('delete/<int:lect_no>', views.lect_delete, name="lect_delete"),
    path('<int:type_no>/search/', views.lect_search, name="lect_search"),
    path('enroll/<int:lect_no>', views.lect_enroll, name="lect_enroll"),  # 신정한 수강생을 강의 명부에 등록하고 lect_room_main 으로 이동
    path('terminate/<int:lect_no>', views.lect_terminate, name="lect_terminate"),
    path('room/<int:room_no>/main/', views.lect_room_main, name="lect_room_main"),  # 강의룸 메인 게시판으로 이동
    path('room/<int:room_no>/search', views.lect_room_search, name="lect_room_search"),

    # 강의 게시글 CRUD
    path('room/<int:room_no>/register/<int:board_type>', views.lect_board_register, name="lect_board_register"),
    path('room/<int:room_no>/detail/<int:lect_board_no>', views.lect_board_detail, name="lect_board_detail"),
    path('room/<int:room_no>/delete/<int:lect_board_no>', views.lect_board_delete, name="lect_board_delete"),
    path('room/<int:room_no>/update/<int:lect_board_no>', views.lect_board_update, name="lect_board_update"),
    path('room/<int:room_no>/list/<int:board_type>', views.lect_room_list, name="lect_room_list"),

    # 과제 제출 CRUD
    path('room/<int:room_no>/assignment/submit', views.lect_assignment_submit, name="lect_assignment_submit"),
    path('room/<int:room_no>/assignment/<int:submit_no>', views.lect_assignment_detail, name="lect_assignment_detail"),
    path('room/<int:room_no>/assignment/<int:submit_no>/update', views.lect_assignment_update,
         name="lect_assignment_update"),
    path('room/<int:room_no>/assignment/<int:submit_no>/delete', views.lect_assignment_delete,
         name="lect_assignment_delete"),
    path('room/<int:room_no>/assignment/', views.lect_assignment_list, name="lect_assignment_list"),  # 리스트

    # 수강생 전용 url
    path('room/<int:room_no>/attend/', views.lect_room_student_status, name="lect_room_student_status"),  # 출석 및 과제 확인
    path('room/<int:room_no>/exit', views.lect_room_exit, name="lect_room_exit"),

    # 강의자 전용 url
    path('room/<int:room_no>/assignment/<int:submit_no>/aor', views.lect_assignment_aor, name="lect_assignment_aor"),
    path('room/<int:room_no>/manage/attendance', views.lect_room_manage_attendance, name="lect_room_manage_attendance"),
    path('room/<int:room_no>/manage/assignment', views.lect_room_manage_assignment, name="lect_room_manage_assignment"),
    path('room/<int:room_no>/manage/member', views.lect_room_manage_member, name="lect_room_manage_member"),
]
