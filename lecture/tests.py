from django.http import HttpRequest
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
    def test_for_getting_all_lectBoards_in_a_lecture_room(self):
        """
                강의자 메뉴 中 : 출석 및 과제 페이지에서 상단 회차별 강의 제목

        """
        lect_room = Lect.objects.prefetch_related("lectures").first()
        lect_board_title_list = [lecture.lect_board_title for lecture in lect_room.lectures.filter(lect_board_type_no=2)]

        request = get_session_request()
        response = lect_room_attend_teacher(request, lect_room.lect_no)

        for lect_title in lect_board_title_list:
            self.assertIn(lect_title, response.content.decode())