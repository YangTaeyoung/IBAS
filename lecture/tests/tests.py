from django.db import connection
from django.test import TestCase
from django.urls import reverse
from DB.models import Lect
from lecture.tests.setup_data import _TestData, save_session


# 출석관리
class LectAttendanceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _TestData()

    def test_for_getting_all_lectBoards_of_a_lecture(self):
        """
                강의자 메뉴 中 : 출석 페이지, 상단 회차별 강의 제목
        """

        lect_room = Lect.objects.prefetch_related("lectures").get(lect_title=_TestData._TEST_TITLE)
        lect_board_list = lect_room.lectures.filter(lect_board_type_id=2).order_by('-lect_board_no')

        save_session(self)
        response = self.client.get(reverse('lect_room_manage_attendance', args=[lect_room.lect_no]))

        self.assertQuerysetEqual(lect_board_list, response.context['lect_board_list'], transform=lambda x: x)

    # def test_check_attendance_info_of_all_students(self):
    #     """
    #             강의자 메뉴 中 : 출석 페이지, 수강생 이름 + 학번 + 출석여부 띄우기
    #     """
    #     lect_room = Lect.objects.prefetch_related("enrolled_students", "lectures"
    #                                               ).get(lect_title=_TestData._TEST_TITLE)
    #     lect_board = lect_room.lectures.first()
    #     query = f"""
    #                         SELECT
    #                             u.USER_NAME,
    #                             u.USER_STU,
    #                             MAJOR_INFO.MAJOR_NAME,
    #                             if(isnull(attend.LECT_ATTEND_DATE),false,true) as attendance
    #                         FROM LECT_ENROLLMENT AS enrollment
    #
    #                         LEFT OUTER JOIN
    #                             LECT_ATTENDANCE AS attend
    #                             on (enrollment.STUDENT = attend.STUDENT AND attend.LECT_BOARD_NO = {lect_board.lect_board_no})
    #
    #                         INNER JOIN
    #                             USER as u ON (enrollment.STUDENT = u.USER_STU),
    #                             MAJOR_INFO
    #
    #                         WHERE
    #                             enrollment.LECT_NO = {lect_room.lect_no}
    #                             and u.USER_MAJOR = MAJOR_INFO.MAJOR_NO
    #
    #                         ORDER BY u.USER_NAME ;"""
    #
    #     cursor = connection.cursor()
    #     cursor.execute(query)  # 쿼리 수행
    #     students_list = [{'index': i + 1, 'name': name, 'stu': stu, 'major': major, 'attendance': '출석' if attendance == 1 else '결석'}
    #                      for i, (name, stu, major, attendance) in enumerate(cursor.fetchall())]
    #
    #     save_session(self)
    #     response = self.client.get(reverse('lect_room_manage_attendance', args=[lect_room.lect_no]))
    #
    #     for index, obj in enumerate(response.context['students_list']):
    #         self.assertDictEqual(students_list[index], obj)


# 과제 관리
class LectAssignmentManageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _TestData()


# 수강생 관리
class ManageMemberTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _TestData()


# 수강생 과제 제출
class AssignmentSubmitTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _TestData()
