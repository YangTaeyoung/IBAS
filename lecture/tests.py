from django.http import HttpRequest
from django.test import TestCase
from DB.models import Lect
from lecture.views import lect_room_attend_teacher
import lecture


class LectBoardTest(TestCase):
    def test_for_getting_all_lectBoards_in_a_lecture_room(self):
        """
                강의자 메뉴 中 : 출석 및 과제 페이지에서 상단 회차별 강의 제목

        """
        lect_room = Lect.objects.prefetch_related("lectures").first()
        lect_board_title_list = [lecture.lect_board_title for lecture in lect_room.lectures.filter(lect_board_type_no=2)]

        request = HttpRequest()
        response = lect_room_attend_teacher(request, lect_room.lect_no)

        for lect_title in lect_board_title_list:
            self.assertIn(lect_title, response.content.decode())