from unittest import skip

from django.db import connection
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import reverse
from django.utils.datetime_safe import date, datetime
from pytz import timezone

from DB.models import Lect, User, LectBoard, LectBoardType, LectEnrollment
from lecture.views import lect_room_attend_teacher
from django.conf import settings
from importlib import import_module


class LectBoardTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        try:
            # 새로운 강의를 등록한다.
            lecture = Lect.objects.create(lect_title="빠르게 시작하는 파이썬", lect_type_id=1, lect_chief_id=12162359,
                                          lect_place_or_link='link', lect_method_id=1, lect_limit_num=60,
                                          lect_deadline=datetime(2021, 7, 29).astimezone(timezone('Asia/Seoul')),
                                          lect_intro='파이썬은 재밌어요', lect_state_id=3)

            # 강의에 게시글이 3개 생긴다.
            LectBoard.objects.create(lect_no=lecture, lect_board_title='첫번째 강의: 파이썬 조건문',
                                     lect_board_writer_id=12162359, lect_board_cont="1234", lect_board_type_id=2)
            LectBoard.objects.create(lect_no=lecture, lect_board_title='두번째 강의: 파이썬 반복문을 알아보자',
                                     lect_board_writer_id=12162359, lect_board_cont="1234", lect_board_type_id=2)
            LectBoard.objects.create(lect_no=lecture, lect_board_title='세번째 강의: 파이썬 객체를 배우자',
                                     lect_board_writer_id=12162359, lect_board_cont="1234", lect_board_type_id=2)

            # 수강생이 들어왔다.
            for std in User.objects.all():
                LectEnrollment.objects.create(lect_no=lecture, student=std)

        except Exception as e:
            raise e

    def test_response_200_for_attendance_page(self):
        """
                강의자 메뉴 中 : 출석 페이지, 수강자 출석 정보 조회 시도 (GET)
        """
        lect_room = Lect.objects.first()

        response = self.client.get(reverse('lect_room_attend_teacher', kwargs={'room_no': lect_room.lect_no}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lecture_room_attend_teacher.html')

    def test_for_getting_all_lectBoards_of_a_lecture(self):
        """
                강의자 메뉴 中 : 출석 페이지, 상단 회차별 강의 제목
        """

        lect_room = Lect.objects.prefetch_related("lectures").first()
        lect_board_list = lect_room.lectures.filter(lect_board_type_id=2).order_by('-lect_board_no')

        response = self.client.get(reverse('lect_room_attend_teacher', kwargs={'room_no': lect_room.lect_no}))

        self.assertQuerysetEqual(lect_board_list, response.context['lect_board_list'], transform=lambda x: x)

    def test_check_attendance_info_of_all_students(self):
        """
                강의자 메뉴 中 : 출석 페이지, 수강생 이름 + 학번 + 출석여부 띄우기
        """
        lect_room = Lect.objects.prefetch_related("enrolled_students", "lectures").first()
        lect_board = lect_room.lectures.first()
        query = f"""SELECT u.USER_NAME, u.USER_STU, if(isnull(attend.LECT_ATTEND_DATE),false,true) as attendance
                    FROM LECT_ENROLLMENT AS enrollment

                    LEFT OUTER JOIN LECT_ATTENDANCE AS attend
                    on (enrollment.STUDENT = attend.STUDENT AND attend.LECT_BOARD_NO = {lect_board.lect_board_no})

                    INNER JOIN USER as u
                    ON (enrollment.STUDENT = u.USER_STU)

                    WHERE enrollment.LECT_NO = {lect_room.lect_no}

                    ORDER BY u.USER_NAME ASC;"""
        cursor = connection.cursor()
        cursor.execute(query)  # 쿼리 수행
        students_list = [{'name': name, 'stu': stu, 'attendance': '출석' if attendance == '1' else '결석'}
                         for name, stu, attendance in cursor.fetchall()]

        response = self.client.get(reverse('lect_room_attend_teacher', kwargs={'room_no': lect_room.lect_no}))

        self.assertListEqual(students_list, response.context['students_list'])

    def test_response_302_for_update_attendance_info(self):
        """
                강의자 메뉴 中 : 출석 페이지, 출석 & 결석 정보 변경 요청 시도 (POST)
        """
        lect_room = Lect.objects.filter(lect_chief_id=12162359).last()
        context = {
            'lect_board_no_': lect_room.lectures.first().lect_board_no
        }

        # 어떤 수강생도 체크하지 않았을 때,
        response = self.client.post(reverse('lect_room_attend_teacher', kwargs={'room_no': lect_room.lect_no}), context)

        self.assertEqual(response.status_code, 302)

