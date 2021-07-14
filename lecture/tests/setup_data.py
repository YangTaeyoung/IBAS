from django.utils.datetime_safe import datetime
from pytz import timezone
from DB.models import Lect, User, LectBoard, LectEnrollment, LectAttendance, LectAssignmentSubmit

_TEST_TITLE = '빠르게 시작하는 파이썬*$%^'
_TEST_LECTURE_CHIEF = User.objects.get(pk=12162359)
_TEST_ASSIGNMENT_TITLE = '과제: 배그를 만들어 오시오#$%^&'
_TEST_STUDENT = User
if (stu := User.objects.filter(user_stu=12171652).first()) is not None:
    _TEST_STUDENT = stu
else:
    _TEST_STUDENT = User.objects.create(user_stu=12171652)


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
        assi = LectBoard.objects.create(lect_no=lecture, lect_board_title=_TEST_ASSIGNMENT_TITLE,
                                 lect_board_writer=_TEST_LECTURE_CHIEF, lect_board_cont="1234", lect_board_type_id=3,
                                 lect_board_ref=ref)

        # 수강생이 들어왔다.
        LectEnrollment.objects.create(lect_no=lecture, student=_TEST_STUDENT)

        # 한 수강생이 수업을 들었다.
        LectAttendance.objects.create(lect_no=lecture, lect_board_no=ref, student=LectEnrollment.objects.first().student)

        # 수강생이 과제를 제출했다.
        LectAssignmentSubmit.objects.create(lect_no=lecture, assignment_no=assi, assignment_submitter=_TEST_STUDENT)

    except Exception as e:
        raise e


def save_sesssion(self, chief=True):
    session = self.client.session
    if chief:
        session["user_stu"] = _TEST_LECTURE_CHIEF.user_stu
    else:
        session["user_stu"] = _TEST_STUDENT.user_stu
    session.save()