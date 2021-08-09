from django.test import TestCase

from django.urls import reverse, resolve
from faker import Faker

from DB.models import Lect, LectBoard, LectEnrollment, LectAssignmentSubmit
from lecture.tests.setup_data import _TestData, save_session


# 강의 CRUD
class LectTest(TestCase):
    def test_response_200_for_Lecture_list(self):
        pass

    def test_response_200_for_Lecture_register(self):
        pass

    def test_response_200_for_Lecture_delete(self):
        pass

    def test_response_200_for_Lecture_update(self):
        pass

    def test_response_302_for_Lecture_register(self):
        pass

    def test_response_302_for_Lecture_delete(self):
        pass

    def test_response_302_for_Lecture_update(self):
        pass


# 강의게시글 CRUD
class LectBoardTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _TestData()

    def test_response_200_for_main_view(self):
        """
                강의자와 수강생, 각각 강의실 메인페이지 접속
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)

        for i in range(2):
            save_session(self) if i == 0 else save_session(self, chief=False)
            response = self.client.get(reverse('lect_room_main', args=[lect_room.lect_no]))

            self.assertEqual(200, response.status_code)
            self.assertTemplateUsed(response, 'lecture_room_main.html')

    def test_response_200_for_LectBoard_list_view(self):
        """
                강의자와 수강생, 각각 (공지사항 목록 + 강의게시글 목록 + 과제 목록) 접근
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)

        for i in range(2):
            save_session(self) if i == 0 else save_session(self, chief=False)

            for lect_board_type in range(1, 4):
                response = self.client.get(
                    reverse('lect_room_list', args=[lect_room.lect_no, lect_board_type])
                )

                self.assertEqual(200, response.status_code)
                self.assertTemplateUsed(response, 'lecture_room_board_list.html')

    def test_response_200_for_LectBoard_detail_view(self):
        """
                강의자와 수강생, 각각 (공지사항 + 강의게시글 + 과제) 조회
        """
        lect_room = Lect.objects.prefetch_related('lectures').get(lect_title=_TestData._TEST_TITLE)
        lect_board_list = lect_room.lectures.all()

        for j in range(2):
            save_session(self) if j == 0 else save_session(self, chief=False)

            for i in lect_board_list:
                response = self.client.get(
                    reverse('lect_board_detail', args=[lect_room.lect_no, i.lect_board_no])
                )

                self.assertEqual(200, response.status_code)
                self.assertTemplateUsed(response, 'lecture_room_board_detail.html')

    def test_response_200_for_LectBoard_register(self):
        """
                강의자, 게시글 등록하기 위해 '글쓰기' 버튼 누름
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)

        save_session(self)
        for board_type in range(1, 4):
            response = self.client.get(
                reverse('lect_board_register', args=[lect_room.lect_no, board_type])
            )

            self.assertEqual(200, response.status_code)
            self.assertTemplateUsed(response, 'lecture_room_board_register.html')

    def test_response_404_for_LectBoard_register_by_bad_student(self):
        """
                수강생, 게시글 등록하기 위해 url jumping 해킹 시도. 404 에러
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)

        save_session(self, chief=False)
        for board_type in range(1, 4):
            response = self.client.get(
                reverse('lect_board_register', args=[lect_room.lect_no, board_type])
            )
            self.assertEqual(404, response.status_code)

    def test_response_200_for_LectBoard_update(self):
        """
                강의자, 게시글 수정하기 위해 '수정하기' 버튼 누름
        """
        lect_room = Lect.objects.prefetch_related('lectures').get(lect_title=_TestData._TEST_TITLE)
        lect_board_list = lect_room.lectures.all()

        save_session(self)
        for i in lect_board_list:
            response = self.client.get(
                reverse('lect_board_update', args=[lect_room.lect_no, i.lect_board_no])
            )

            self.assertEqual(200, response.status_code)
            self.assertTemplateUsed(response, 'lecture_room_board_register.html')

    def test_response_404_for_LectBoard_update_by_student(self):
        """
                수강생, 게시글 수정하기 위해 url jumping 해킹 시도, 404 에러
        """
        lect_room = Lect.objects.prefetch_related('lectures').get(lect_title=_TestData._TEST_TITLE)
        lect_board_list = lect_room.lectures.all()

        save_session(self, chief=False)
        for i in lect_board_list:
            response = self.client.get(
                reverse('lect_board_update', args=[lect_room.lect_no, i.lect_board_no])
            )

            self.assertEqual(404, response.status_code)

    def test_response_302_for_LectBoard_register(self):
        """
                강의자, 게시글 등록함.
        """
        fake = Faker()
        save_session(self)
        session = self.client.session
        session["user_stu"] = _TestData._TEST_LECTURE_CHIEF.user_stu
        for i in range(1, 4):
            board = {
                'lect_board_type_id': i,
                'lect_board_writer': _TestData._TEST_LECTURE_CHIEF,
                'lect_board_title': fake.word(),
                'lect_board_cont': fake.text(),
            }
            response = self.client.post(
                reverse('lect_board_register', args=[Lect.objects.get(lect_title=_TestData._TEST_TITLE).lect_no, i]),
                data=board
            )
            self.assertEqual(302, response.status_code)

    def test_response_302_for_LectBoard_update(self):
        """
                강의자, 게시글 수정함
        """
        fake = Faker()
        save_session(self)
        lecture = Lect.objects.get(lect_title=_TestData._TEST_TITLE)
        for i in range(1, 4):
            board = LectBoard.objects.filter(lect_no=lecture, lect_board_type_id=i).first()
            data = {
                'lect_board_type_id': i,
                'lect_board_writer': _TestData._TEST_LECTURE_CHIEF,
                'lect_board_title': fake.word(),
                'lect_board_cont': fake.text(),
            }
            response = self.client.post(
                reverse('lect_board_update', args=[lecture.lect_no, board.lect_board_no]),
                data=data
            )
            self.assertEqual(302, response.status_code)

    def test_response_302_for_LectBoard_delete(self):
        """
                강의자, 게시글 삭제함.
        """
        lect_room = Lect.objects.prefetch_related('lectures').get(lect_title=_TestData._TEST_TITLE)
        lect_board_list = lect_room.lectures.exclude(lect_board_type_id=3)

        save_session(self)
        for i in lect_board_list:
            response = self.client.get(
                reverse('lect_board_delete', args=[lect_room.lect_no, i.lect_board_no])
            )

            self.assertEqual(302, response.status_code)


# 출석관리
class LectAttendanceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _TestData()

    def test_response_200_for_attendance_page(self):
        """
                강의자 메뉴 中 : 출석 페이지, 수강자 출석 정보 조회 시도 (GET)
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)

        save_session(self)
        response = self.client.get(reverse('lect_room_manage_attendance', args=[lect_room.lect_no]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lecture_room_manage_attendance.html')

    def test_response_302_for_update_attendance_info(self):
        """
                강의자 메뉴 中 : 출석 페이지, 출석 & 결석 정보 변경 요청 시도 (POST)
        """
        lect_room = Lect.objects.filter(lect_title=_TestData._TEST_TITLE).first()
        context = {
            'lect_board_no_': lect_room.lectures.first().lect_board_no
        }

        # 어떤 수강생도 체크하지 않았을 때,
        save_session(self)
        response = self.client.post(reverse('lect_room_manage_attendance', args=[lect_room.lect_no]), context)

        self.assertEqual(response.status_code, 302)

    def test_response_404_for_attendance_page_by_bad_student(self):
        """
                수강생 : 출석 페이지, 수강자 출석 정보 url jumping 해킹 시도 (GET)
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)

        save_session(self, chief=False)
        response = self.client.get(reverse('lect_room_manage_attendance', args=[lect_room.lect_no]))

        self.assertEqual(response.status_code, 404)


# 과제 관리
class LectAssignmentManageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _TestData()

    def test_response_200_for_assignment_manage_html(self):
        """
                강의자 메뉴 中 : 수강생 과제 관리 페이지 접속
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)

        save_session(self)
        response = self.client.get(reverse('lect_room_manage_assignment', args=[lect_room.lect_no]))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'lecture_room_manage_assignment.html')

    def test_response_302_for_assignment_manage_html(self):
        """
                        강의자 메뉴 中 : 수강생 과제 사항 변경 시도
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)
        save_session(self)

        response = self.client.post(reverse('lect_room_manage_assignment', args=[lect_room.lect_no]), data={'manage_mode': '1'})

        self.assertEqual(302, response.status_code)

    def test_response_404_for_assignment_manage_html_by_bad_student(self):
        """
                수강생 : 수강생 과제 관리 페이지 url jumping 해킹 시도
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)

        save_session(self, chief=False)
        response = self.client.get(reverse('lect_room_manage_assignment', args=[lect_room.lect_no]))

        self.assertEqual(404, response.status_code)


# 수강생 관리
class ManageMemberTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _TestData()

    def test_response_200_for_member_manage_html(self):
        """
                강의자 메뉴 中 : 수강생 관리 페이지 접속
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)

        save_session(self)
        response = self.client.get(reverse('lect_room_manage_member', args=[lect_room.lect_no]))

        self.assertEqual(200, response.status_code)

    def test_response_302_for_member_manage(self):
        """
                강의자 메뉴 中 : 수강생 관리 페이지, 수강생 정보 변경
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)
        save_session(self)
        for status_mode in range(2):
            context = {
                'is_checked_' + str(_TestData._TEST_STUDENT): LectEnrollment.objects.get(lect_no=lect_room.lect_no, student_id=_TestData._TEST_STUDENT).pk,
                'status_mode': status_mode
            }

            response = self.client.post(reverse('lect_room_manage_member', args=[lect_room.lect_no]), context)

            self.assertEqual(302, response.status_code)

    def test_response_404_for_member_manage_html_by_bad_student(self):
        """
                수강생 : 수강생 관리 페이지 url jumping 해킹 시도
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)

        save_session(self, chief=False)
        response = self.client.get(reverse('lect_room_manage_member', args=[lect_room.lect_no]))

        self.assertEqual(404, response.status_code)

    def test_response_200_for_student_status(self):
        """
                수강생 메뉴 中 : 수강생 출석 및 과제 제출 현황 조회
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)

        save_session(self, chief=False)
        response = self.client.get(reverse('lect_room_student_status', args=[lect_room.lect_no]))

        self.assertEqual(200, response.status_code)


# 수강생 과제 제출 CRUD
class AssignmentSubmitTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        _TestData()

    def test_response_200_for_submit_html(self):
        """
                수강생 과제 제출 페이지 접근
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)
        assignment = LectBoard.objects.get(lect_board_title=_TestData._TEST_ASSIGNMENT_TITLE)

        save_session(self, chief=False)
        response = self.client.get(
            reverse('lect_assignment_submit', args=[lect_room.lect_no]),
            data={'lect_board_no': assignment.lect_board_no}
        )

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'lecture_assignment_submit.html')

    def test_response_200_for_submitted_assignment_detail(self):
        """
                수강생 제출한 과제 확인
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)
        assignment = LectAssignmentSubmit.objects.get(assignment_submitter=_TestData._TEST_STUDENT, lect_no=lect_room)

        save_session(self, chief=False)
        response = self.client.get(
            reverse('lect_assignment_detail', args=[lect_room.pk, assignment.pk])
        )

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'lecture_assignment_detail.html')

    def test_response_200_for_update_submitted_assignment(self):
        """
                수강생 제출한 과제 수정 시도
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)
        assignment = LectAssignmentSubmit.objects.get(assignment_submitter=_TestData._TEST_STUDENT, lect_no=lect_room)

        save_session(self, chief=False)
        response = self.client.get(
            reverse('lect_assignment_update', args=[lect_room.pk, assignment.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lecture_assignment_submit.html')

    def test_response_302_for_delete_submitted_assignment(self):
        """
                수강생 제출한 과제 삭제 시도
        """
        lect_room = Lect.objects.get(lect_title=_TestData._TEST_TITLE)
        assignment = LectAssignmentSubmit.objects.get(assignment_submitter=_TestData._TEST_STUDENT, lect_no=lect_room)

        save_session(self, chief=False)
        response = self.client.get(
            reverse('lect_assignment_delete', args=[lect_room.pk, assignment.pk])
        )
        self.assertRedirects(response, f'lect/room/{lect_room.pk}/assignment', status_code=302)

    def test_response_302_for_submit_assignment(self):
        pass

    def test_response_302_for_update_submitted_assignment(self):
        pass

    def test_response_302_for_delete_submitted_assignment(self):
        pass


