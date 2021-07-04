from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from DB.models import Lect
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
    def test_for_getting_all_lectBoards_of_a_lecture(self):
        """
                강의자 메뉴 中 : 출석 및 과제 페이지에서 상단 회차별 강의 제목
        """

        lect_room = Lect.objects.prefetch_related("lectures").first()
        lect_board_title_list = [lecture.lect_board_title for lecture in lect_room.lectures.filter(lect_board_type_no=2)]

        request = get_session_request()
        response = lect_room_attend_teacher(request, lect_room.lect_no)

        for lect_title in lect_board_title_list:
            self.assertIn(lect_title, response.content.decode(),
                          msg="강의자 출석&과제 관리 메뉴: 강의 게시글 불러오기 실패")

    def test_for_getting_all_student_of_a_lecture(self):
        """
               강의자 메뉴 中 : 출석 및 과제 페이지에서 수강생 이름 및 학번 리스트 띄우기
        """

        lect_room = Lect.objects.prefetch_related("enrolled_students").first()
        students_list = [(row.student.user_name, row.student.user_stu) for row in lect_room.enrolled_students.all()]

        request = get_session_request()
        response = lect_room_attend_teacher(request, lect_room.lect_no)
        expected_html = render_to_string('_table_attendence_check.html', {'students_list': lect_room.enrolled_students.all()})

        self.assertIn(expected_html, response.content.decode(),
                      msg="강의자 출석&과제 관리 메뉴: 학생 정보 불러오기 실패")
