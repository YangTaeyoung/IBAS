from unittest import skip

from django.db import connection
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import reverse

from DB.models import Lect, User, LectBoard, LectBoardType, LectEnrollment
from lecture.views import lect_room_attend_teacher
from django.conf import settings
from importlib import import_module


def get_session_request():
    """
        django test 시에는 middleware 가 작동하지 않는듯함.
        수동으로 세션을 설정하지 않으면, 테스트 불가!
        딕셔너리 객체로 할당해도 되지만, 세션엔진을 임포트해서 저장했음.
    """
    request = HttpRequest()
    engine = import_module(settings.SESSION_ENGINE)
    session_key = None
    request.session = engine.SessionStore(session_key)
    return request


class LectBoardTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        try:
            # 새로운 강의를 등록한다.
            lecture = Lect.objects.create(lect_title="빠르게 시작하는 파이썬", lect_type_id=1, lect_chief_id=12162359,
                                          lect_place_or_link='link', lect_method_id=1, lect_deadline="2021-07-29",
                                          lect_intro='파이썬은 재밌어요', lect_state_id=3, lect_limit_num=60)

            # 강의에 게시글이 3개 생긴다.
            LectBoard.objects.create(lect_no=lecture, lect_board_title='첫번째 강의: 파이썬 조건문',
                                     lect_board_writer_id=12162359, lect_board_cont="1234", lect_board_type_no_id=2)
            LectBoard.objects.create(lect_no=lecture, lect_board_title='두번째 강의: 파이썬 반복문을 알아보자',
                                     lect_board_writer_id=12162359, lect_board_cont="1234", lect_board_type_no_id=2)
            LectBoard.objects.create(lect_no=lecture, lect_board_title='세번째 강의: 파이썬 객체를 배우자',
                                     lect_board_writer_id=12162359, lect_board_cont="1234", lect_board_type_no_id=2)

            # 수강생이 들어왔다.
            LectEnrollment.objects.create(lect_no=Lect.objects.first(), student_id=12171652)
            LectEnrollment.objects.create(lect_no=Lect.objects.first(), student_id=12111223)
            LectEnrollment.objects.create(lect_no=Lect.objects.first(), student_id=12151251)
            LectEnrollment.objects.create(lect_no=Lect.objects.first(), student_id=12172285)
            LectEnrollment.objects.create(lect_no=Lect.objects.first(), student_id=12172434)
            LectEnrollment.objects.create(lect_no=Lect.objects.first(), student_id=12192199)
            LectEnrollment.objects.create(lect_no=Lect.objects.first(), student_id=12192355)
            LectEnrollment.objects.create(lect_no=Lect.objects.first(), student_id=15156126)

        except Exception as e:
            raise e

    def test_response_200_for_attendance_page(self):
        """
                강의자 메뉴 中 : 출석 페이지, 수강자 출석 정보 조회 시도
        """
        lect_room = Lect.objects.first()

        response = self.client.get(reverse('lect_room_attend_teacher', kwargs={'room_no': lect_room.lect_no}))
        self.assertEqual(response.status_code, 200, msg='lect/room/%s/attend/teacher' % lect_room.lect_no)

    def test_for_getting_all_lectBoards_of_a_lecture(self):
        """
                강의자 메뉴 中 : 출석 페이지, 상단 회차별 강의 제목
        """

        lect_room = Lect.objects.prefetch_related("lectures").first()
        lect_board_title_list = [lecture.lect_board_title for lecture in lect_room.lectures.filter(lect_board_type_no=2)]

        response = self.client.get(reverse('lect_room_attend_teacher', kwargs={'room_no': lect_room.lect_no}))

        for lect_title in lect_board_title_list:
            self.assertIn(lect_title, response.content.decode(),
                          msg="강의자 출석 관리 메뉴: 강의 게시글 불러오기 실패")

    def test_for_getting_all_student_of_a_lecture(self):
        """
               강의자 메뉴 中 : 출석 페이지, 수강생 이름 및 학번 리스트 띄우기
        """

        lect_room = Lect.objects.prefetch_related("enrolled_students").first()
        students_list = [row.student.user_name for row in lect_room.enrolled_students.all()]

        response = self.client.get(reverse('lect_room_attend_teacher', kwargs={'room_no': lect_room.lect_no}))

        for name in students_list:
            self.assertIn(name, response.content.decode(),
                          msg="수강생 정보 불러오기 실패")

    def test_check_attendance_of_every_student(self):
        """
                강의자 메뉴 中 : 출석 페이지, 출석여부 띄우기
        """
        lect_room = Lect.objects.prefetch_related("enrolled_students", "lectures").first()
        lect_board_list = lect_room.lectures.all().order_by('-lect_board_no')
        query = """SELECT u.USER_NAME, u.USER_STU, if(isnull(attend.ATTEND_DATE),false,true) as attendance
                    FROM LECT_ENROLLMENT AS enrollment

                    LEFT OUTER JOIN LECT_ATTENDANCE AS attend
                    on (enrollment.STUDENT = attend.STUDENT AND attend.LECT_BOARD_NO = %s)

                    INNER JOIN USER as u
                    ON (enrollment.STUDENT = u.USER_STU)

                    WHERE enrollment.LECT_NO = %s

                    ORDER BY u.USER_NAME ASC;""" % (lect_board_list[0].lect_board_no, lect_room.lect_no)
        cursor = connection.cursor()
        cursor.execute(query)  # 쿼리 수행
        students_list = [{'name': name, 'stu': stu, 'attendance': '출석' if attendance == '1' else '결석'}
                         for name, stu, attendance in cursor.fetchall()]

        response = self.client.get(reverse('lect_room_attend_teacher', kwargs={'room_no': lect_room.lect_no}))
        expected_html = render_to_string('_table_attendence_check.html', {'students_list': students_list})

        self.assertIn(expected_html, response.content.decode())

    @skip
    def test_post_request_for_update_attendance_info(self):
        pass

