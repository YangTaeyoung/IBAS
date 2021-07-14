from unittest import skip
from unittest.mock import patch

from django.core.handlers.wsgi import WSGIRequest
from django.db import connection
from django.db.models import Q
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import reverse
from django.utils.datetime_safe import date, datetime
from pytz import timezone
from DB.models import Lect, User, LectBoard, LectBoardType, LectEnrollment, LectAttendance
from faker import Faker
from lecture.tests.setup_data import *
from lecture.tests.setup_data import _test_data, _TEST_TITLE, _TEST_LECTURE_CHIEF, _TEST_ASSIGNMENT_TITLE


# 출석관리
class LectAttendanceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _test_data()

    def test_for_getting_all_lectBoards_of_a_lecture(self):
        """
                강의자 메뉴 中 : 출석 페이지, 상단 회차별 강의 제목
        """

        lect_room = Lect.objects.prefetch_related("lectures").get(lect_title=_TEST_TITLE)
        lect_board_list = lect_room.lectures.filter(lect_board_type_id=2).order_by('-lect_board_no')

        save_sesssion(self)
        response = self.client.get(reverse('lect_room_manage_attendance', args=[lect_room.lect_no]))

        self.assertQuerysetEqual(lect_board_list, response.context['lect_board_list'], transform=lambda x: x)

    def test_check_attendance_info_of_all_students(self):
        """
                강의자 메뉴 中 : 출석 페이지, 수강생 이름 + 학번 + 출석여부 띄우기
        """
        lect_room = Lect.objects.prefetch_related("enrolled_students", "lectures"
                                                  ).filter(lect_title=_TEST_TITLE).first()
        lect_board = lect_room.lectures.first()
        query = f"""SELECT u.USER_NAME, u.USER_STU, if(isnull(attend.LECT_ATTEND_DATE),false,true) as attendance
                    FROM LECT_ENROLLMENT AS enrollment

                    LEFT OUTER JOIN LECT_ATTENDANCE AS attend
                    on (enrollment.STUDENT = attend.STUDENT AND attend.LECT_BOARD_NO = {lect_board.lect_board_no})

                    INNER JOIN USER as u
                    ON (enrollment.STUDENT = u.USER_STU)

                    WHERE enrollment.LECT_NO = {lect_room.lect_no}

                    ORDER BY u.USER_NAME;"""
        cursor = connection.cursor()
        cursor.execute(query)  # 쿼리 수행
        students_list = [{'name': name, 'stu': stu, 'attendance': '출석' if attendance == 1 else '결석'}
                         for name, stu, attendance in cursor.fetchall()]

        save_sesssion(self)
        response = self.client.get(reverse('lect_room_manage_attendance', args=[lect_room.lect_no]))

        self.assertListEqual(students_list, response.context['students_list'])


# 과제 관리
class LectAssignmentManageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _test_data()




# 수강생 관리
class ManageMemberTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _test_data()



# 수강생 과제 제출
class AssignmentSubmitTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _test_data()
