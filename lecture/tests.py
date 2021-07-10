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
from member.session import save_session
from faker import Faker

_TEST_TITLE = '빠르게 시작하는 파이썬*$%^'
_TEST_LECTURE_CHIEF = User.objects.get(pk=12162359)


def _test_data():
    try:
        # 새로운 강의를 등록한다.
        lecture = Lect.objects.create(lect_title=_TEST_TITLE, lect_type_id=1, lect_chief=_TEST_LECTURE_CHIEF,
                                      lect_place_or_link='link', lect_method_id=1, lect_limit_num=60,
                                      lect_deadline=datetime(2021, 7, 29).astimezone(timezone('Asia/Seoul')),
                                      lect_intro='파이썬은 재밌어요', lect_state_id=3)

        # 게시글이 3개 생긴다.
        ref = LectBoard.objects.create(lect_no=lecture, lect_board_title='첫번째 강의: 파이썬 조건문',
                                    lect_board_writer=_TEST_LECTURE_CHIEF, lect_board_cont="1234", lect_board_type_id=2)
        LectBoard.objects.create(lect_no=lecture, lect_board_title='공지사항',
                                 lect_board_writer=_TEST_LECTURE_CHIEF, lect_board_cont="1234", lect_board_type_id=1)
        LectBoard.objects.create(lect_no=lecture, lect_board_title='과제: 배그를 만들어 오시오',
                                 lect_board_writer=_TEST_LECTURE_CHIEF, lect_board_cont="1234", lect_board_type_id=3,
                                 lect_board_ref=ref)

        # 수강생이 들어왔다.
        for std in User.objects.all():
            LectEnrollment.objects.create(lect_no=lecture, student=std)

        # 한 수강생이 수업을 들었다.
        LectAttendance.objects.create(lect_no=lecture, lect_board_no=ref, student=LectEnrollment.objects.first().student)

    except Exception as e:
        raise e


# 강의 게시글 CRUD
class LectBoardTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _test_data()

    def test_response_200_for_main_view(self):
        lect_room = Lect.objects.get(lect_title=_TEST_TITLE)
        response = self.client.get(reverse('lect_room_main', kwargs={'room_no': lect_room.lect_no}))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'lecture_room_main.html')

    def test_response_200_for_LectBoard_list_view(self):
        lect_room = Lect.objects.get(lect_title=_TEST_TITLE)

        for lect_board_type in range(1,4):
            response = self.client.get(
                reverse('lect_room_list', kwargs={'room_no': lect_room.lect_no, 'board_type': lect_board_type})
            )

            self.assertEqual(200, response.status_code)
            self.assertTemplateUsed(response, 'lecture_room_board_list.html')

    def test_response_200_for_LectBoard_detail_view(self):
        lect_room = Lect.objects.prefetch_related('lectures').get(lect_title=_TEST_TITLE)
        lect_board_list = lect_room.lectures.all()

        for i in lect_board_list:
            response = self.client.get(
                reverse('lect_board_detail', kwargs={'room_no': lect_room.lect_no, 'board_no': i.lect_board_no})
            )

            self.assertEqual(200, response.status_code)
            self.assertTemplateUsed(response, 'lecture_room_board_detail.html')

    def test_response_200_for_LectBoard_register(self):
        lect_room = Lect.objects.get(lect_title=_TEST_TITLE)

        for board_type in range(1, 4):
            response = self.client.get(
                reverse('lect_board_register', kwargs={'room_no': lect_room.lect_no, 'board_type': board_type})
            )

            self.assertEqual(200, response.status_code)
            self.assertTemplateUsed(response, 'lecture_room_board_register.html')

    def test_response_200_for_LectBoard_update(self):
        lect_room = Lect.objects.prefetch_related('lectures').get(lect_title=_TEST_TITLE)
        lect_board_list = lect_room.lectures.all()

        for i in lect_board_list:
            response = self.client.get(
                reverse('lect_board_update', kwargs={'room_no': lect_room.lect_no, 'board_no': i.lect_board_no})
            )

            self.assertEqual(200, response.status_code)
            self.assertTemplateUsed(response, 'lecture_room_board_register.html')

    def test_response_302_for_LectBoard_register(self):
        fake = Faker()
        session = self.client.session
        session["user_stu"] = _TEST_LECTURE_CHIEF.user_stu
        for i in range(1, 4):
            board = {
                'lect_board_type_id': i,
                'lect_board_writer': _TEST_LECTURE_CHIEF,
                'lect_board_title': fake.word(),
                'lect_board_cont': fake.text(),
            }
            response = self.client.post(
                reverse('lect_board_register', kwargs={'room_no': Lect.objects.get(lect_title=_TEST_TITLE).lect_no, 'board_type': i}),
                data=board
            )
            self.assertEqual(302, response.status_code)

    def test_response_302_for_LectBoard_update(self):
        fake = Faker()
        session = self.client.session
        session["user_stu"] = _TEST_LECTURE_CHIEF.user_stu
        session.save()
        lecture = Lect.objects.get(lect_title=_TEST_TITLE)
        for i in range(1, 4):
            board = LectBoard.objects.filter(lect_no=lecture, lect_board_type_id=i).first()
            data = {
                'lect_board_type_id': i,
                'lect_board_writer': _TEST_LECTURE_CHIEF,
                'lect_board_title': fake.word(),
                'lect_board_cont': fake.text(),
            }
            response = self.client.post(
                reverse('lect_board_update',
                        kwargs={'room_no': lecture.lect_no, 'board_no': board.lect_board_no}),
                data=data
            )
            self.assertEqual(302, response.status_code)

    def test_response_302_for_LectBoard_delete(self):
        lect_room = Lect.objects.prefetch_related('lectures').get(lect_title=_TEST_TITLE)
        lect_board_list = lect_room.lectures.exclude(lect_board_type_id=3)

        for i in lect_board_list:
            response = self.client.get(
                reverse('lect_board_delete', kwargs={'room_no': lect_room.lect_no, 'board_no': i.lect_board_no})
            )

            self.assertEqual(302, response.status_code)


# 출석관리
class LectAttendanceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _test_data()

    def test_response_200_for_attendance_page(self):
        """
                강의자 메뉴 中 : 출석 페이지, 수강자 출석 정보 조회 시도 (GET)
        """
        lect_room = Lect.objects.get(lect_title=_TEST_TITLE)

        response = self.client.get(reverse('lect_room_manage_attendance', kwargs={'room_no': lect_room.lect_no}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lecture_room_manage_attendance.html')

    def test_for_getting_all_lectBoards_of_a_lecture(self):
        """
                강의자 메뉴 中 : 출석 페이지, 상단 회차별 강의 제목
        """

        lect_room = Lect.objects.prefetch_related("lectures").get(lect_title=_TEST_TITLE)
        lect_board_list = lect_room.lectures.filter(lect_board_type_id=2).order_by('-lect_board_no')

        response = self.client.get(reverse('lect_room_manage_attendance', kwargs={'room_no': lect_room.lect_no}))

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

                    ORDER BY u.USER_NAME ASC;"""
        cursor = connection.cursor()
        cursor.execute(query)  # 쿼리 수행
        students_list = [{'name': name, 'stu': stu, 'attendance': '출석' if attendance == 1 else '결석'}
                         for name, stu, attendance in cursor.fetchall()]

        response = self.client.get(reverse('lect_room_manage_attendance', kwargs={'room_no': lect_room.lect_no}))

        self.assertListEqual(students_list, response.context['students_list'])

    def test_response_302_for_update_attendance_info(self):
        """
                강의자 메뉴 中 : 출석 페이지, 출석 & 결석 정보 변경 요청 시도 (POST)
        """
        lect_room = Lect.objects.filter(lect_title=_TEST_TITLE).first()
        context = {
            'lect_board_no_': lect_room.lectures.first().lect_board_no
        }

        # 어떤 수강생도 체크하지 않았을 때,
        response = self.client.post(reverse('lect_room_manage_attendance', kwargs={'room_no': lect_room.lect_no}), context)

        self.assertEqual(response.status_code, 302)


#
class LectAssignmentManageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _test_data()

    def test_response_200_for_assignment_manage_html(self):
        """
                강의자 메뉴 中 : 수강생 과제 관리 페이지 접속
        """
        lect_room = Lect.objects.get(lect_title=_TEST_TITLE)

        response = self.client.get(reverse('lect_room_manage_assignment', args=[lect_room.lect_no]))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'lecture_room_manage_assignment.html')


# 수강생 관리
class ManageMemberTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _test_data()

    def test_response_200_for_member_manage_html(self):
        """
                강의자 메뉴 中 : 수강생 관리 페이지 접속
        """
        lect_room = Lect.objects.get(lect_title=_TEST_TITLE)

        response = self.client.get(reverse('lect_room_manage_member', args=[lect_room.lect_no]))

        self.assertEqual(200, response.status_code)

    def test_response_302_for_member_manage(self):
        """
                강의자 메뉴 中 : 수강생 관리 페이지, 수강생 정보 변경
        """
        lect_room = Lect.objects.get(lect_title=_TEST_TITLE)
        std = lect_room.attendance.first().student.user_stu  # 임의의 한 강의를 들었던 사람의 학번
        for status_mode in range(2):
            context = {
                'is_checked_' + str(std): LectEnrollment.objects.get(lect_no=lect_room.lect_no, student_id=std).pk,
                'status_mode': status_mode
            }

            response = self.client.post(reverse('lect_room_manage_member', args=[lect_room.lect_no]), context)

            self.assertEqual(302, response.status_code)

    def test_response_200_for_student_status(self):
        """
                수강생 메뉴 中 : 수강생 출석 및 과제 제출 현황 조회
        """
        lect_room = Lect.objects.get(lect_title=_TEST_TITLE)
        session = self.client.session
        session['user_stu'] = lect_room.attendance.first().student.user_stu
        session.save()

        response = self.client.get(reverse('lect_room_student_status', args=[lect_room.lect_no]))

        self.assertEqual(200, response.status_code)