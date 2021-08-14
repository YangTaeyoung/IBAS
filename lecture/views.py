from django.db import transaction, connection
from django.db.models import Q
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils.dateformat import DateFormat
from alarm.alarm_controller import create_lect_full_alarm, create_lect_enroll_alarm, delete_lect_by_superuser_alarm, \
    create_user_lect_out_alarm
from django.contrib import messages
from DB.models import LectType, Lect, MethodInfo, LectBoard, LectEnrollment, LectAttendance, \
    LectAssignmentSubmit, LectMoneyStandard, StateInfo
from file_controller import FileController
from lecture.forms import LectForm, LectRejectForm, LectPicForm, make_lect_board_form, \
    FileForm, AssignmentSubmitForm
from pagination_handler import get_page_object
from user_controller import get_logined_user, superuser_only, writer_only, auth_check, is_superuser, \
    is_logined, member_only, role_check, room_enter_check, enroll_check, is_closed, instructor_only, \
    login_required, prohibit_professor, not_allowed
from utils.crawler import get_og_tag
from utils.url_regex import is_youtube
from utils.youtube import get_youtube
from date_controller import is_lect_recruiting, today
from exception_handler import exist_check
from post_controller import comment_delete_by_post_delete, ongoing_check


def get_pol_name(method_no):
    pol_name = MethodInfo.objects.get(pk=method_no).method_name
    if method_no == 1:
        pol_name = "장소"
    elif method_no == 2:
        pol_name = pol_name + " 개인 링크"
    else:
        pol_name = pol_name + " 개인 채널 링크"
    return pol_name


# 타입에 맞는 강의 리스트를 반환하는 함수
def get_lect_list(request, type_no):
    if type_no != 4:  # 강의 개설 신청 게시판이 아닌 일반 게시판(강의, 스터디, 취미모임)의 경우
        # 진행중이거나 마감된 강의
        lect_list = Lect.objects.filter(Q(lect_type_id=type_no) & Q(lect_state_id=3)).prefetch_related(
            "enrolled_students").order_by("lect_deadline")
        # 이미 종료된 강의
        lect_list_end = Lect.objects.filter(Q(lect_type_id=type_no) & Q(lect_state_id=4)).prefetch_related(
            "enrolled_students").order_by("lect_deadline")

        # 마감된 강의를 담을 리스트
        lect_list_expired = list()
        # 아직 모집중인 강의를 담을 리스트
        lect_list_recruiting = list()

        for lect in lect_list:
            # 마감일이 지났거나, 인원이 가득 차면 True
            if is_closed(lect):  
                lect_list_expired.append(lect)  # 마감 리스트에 추가
            # 그렇지 않은 경우, 즉 모집중인 경우
            else:  
                lect_list_recruiting.append(lect)  # 모집 리스트에 추가

        lect_list_recruiting.extend(lect_list_expired)  # 모집 리스트와 마감 리스트를 합침
        lect_list_recruiting.extend(lect_list_end)  # 모집 리스트와 종료 리스트를 합침
        lect_list = lect_list_recruiting  # lect_list를 합친 리스트로 변환 (리턴하고 있는게 lect_list이므로)

    else:  # 강의 개설 신청 게시판의 경우
        # 강의이면서 대기중이거나 거절당한 강의를 가져옴
        lect_list = Lect.objects.filter(Q(lect_type_id=1) & Q(lect_state_id__lte=2)).prefetch_related(
            "enrolled_students").order_by("-lect_created").order_by("lect_state_id")
    return lect_list


# 타입에 맞는 강의 타입 인스턴스를 반환하는 함수
def get_lect_type(request, type_no):
    if type_no != 4:
        lect_type = LectType.objects.get(pk=type_no)
    else:
        if not is_logined(request) or not is_superuser(
                get_logined_user(request)):  # 강의 개설 관련 처리는 관리자만 할 수 있으므로 관리자 권한 체크
            return redirect(reverse("index"))
        lect_type = LectType()
        lect_type.type_no = type_no
        lect_type.type_no = 4
        lect_type.type_name = "강의 개설 신청"
        lect_type.type_exp = "개설 신청된 강의 목록입니다."
    return lect_type


@auth_check(active=True)
def lect_register(request):  # 강의/스터디/취미모임 등록 페이지로 이동하는 것
    if request.method == "GET":
        lect_type = LectType.objects.get(pk=request.GET.get("lect_type"))
        init_dict = {"lect_type": lect_type.type_no, "lect_paid": 0}
        if lect_type.type_no == 1:  # 강의일 때
            if not is_lect_recruiting():
                messages.warning(request, message="강의 등록 기간이 아닙니다.")
                return redirect("lect_view", type_no=lect_type.type_no)
            init_dict.update(lect_state=1)
        else:  # 강의가 아닐 때
            init_dict.update(lect_state=3)

        context = {
            "lect_money_standard": LectMoneyStandard.objects.get(pk=1),
            "lect_type": lect_type,
            "method_list": MethodInfo.objects.all(),
            "lect_form": LectForm(initial=init_dict),
            "lect_pic_form": LectPicForm(),
            "is_update": False,
            "pol_name": get_pol_name(1)
        }
        return render(request, 'lecture_register.html', context)
    else:  # 강의/스터디/취미 모임 폼을 입력하고 전송 버튼을 눌렀을 경우
        lect_form = LectForm(request.POST)
        lect_pic_form = LectPicForm(request.POST, request.FILES)
        # 폼 유효성 검증
        if lect_form.is_valid() and lect_pic_form.is_valid():  # 유효성 검사 성공 시
            lect = lect_form.save(lect_chief=get_logined_user(request))
            lect_pic_form.save(instance=lect)
            lect.lect_day = request.POST.get("lect_day")
            lect.save()
            return redirect("lect_detail", lect_no=lect.lect_no)
        else:  # 유효성 검사 실패 시
            return redirect("lect_view", type_no=1)


# 강의 상세 페이지로 이동 (활동 회원만 가능)
@exist_check
@room_enter_check
def lect_detail(request, lect_no):
    lect = Lect.objects.get(pk=lect_no)
    lect.lect_day = lect.lect_day.replace(" ", ",")
    lect.lect_day = lect.lect_day[:len(lect.lect_day) - 1]
    context = {
        'lect': lect,
        'is_in': LectEnrollment.objects.filter(student=get_logined_user(request),
                                               lect_no_id=lect_no).count() > 0,
        'lect_reject_form': LectRejectForm(instance=lect),
        'is_closed': is_closed(lect)
    }
    # 취미 모임의 경우 강의 방식이 없음 따라서 해당 부분에 대한 예외처리
    if lect.lect_method is not None:
        context.update(pol_name=get_pol_name(lect.lect_method.method_no))
    return render(request, 'lecture_detail.html', context)


@superuser_only()
def lect_aor(request, lect_no):  # 강의 등록 거절 함수
    if request.method == "POST":
        lect_form = LectRejectForm(request.POST)
        if lect_form.is_valid():
            lect_form.update(instance=Lect.objects.get(pk=lect_no))
        return redirect("lect_detail", lect_no=lect_no)
    else:
        return redirect(reverse("index"))


# 강의를 수정하는 함수
@writer_only(superuser=False)
def lect_update(request, lect_no):
    lect = Lect.objects.get(pk=lect_no)
    lect.lect_deadline = DateFormat(lect.lect_deadline).format("Y-m-d")
    if request.method == "POST":  # 폼에 수정데이터를 입력 후 수정 버튼을 눌렀을 때
        lect_form = LectForm(request.POST)
        lect_pic_form = LectPicForm(request.POST, request.FILES)
        if lect_form.is_valid():
            lect = lect_form.update(instance=lect)
            lect.lect_day = request.POST.get("lect_day")
            lect.save()
            if lect_pic_form.is_valid():
                if lect_pic_form.has_changed():
                    FileController.delete_all_files_of_(lect)
                    lect_pic_form.save(instance=lect)
        return redirect("lect_detail", lect_no=lect.lect_no)
    else:  # 상세 페이지에서 수정 버튼을 눌렀을 때
        context = {
            "lect_money_standard": LectMoneyStandard.objects.get(pk=1),
            "lect_type": lect.lect_type,
            "method_list": MethodInfo.objects.all(),
            "lect_form": LectForm(instance=lect),
            "lect_pic_form": LectPicForm(instance=lect),
            "is_update": True,
            "lect_no": lect.lect_no,
            "lect_day": lect.lect_day
        }
        if lect.lect_method is not None:
            context.update(pol_name=get_pol_name(lect.lect_method.method_no))
        return render(request, "lecture_register.html", context)


# 강의 삭제 함수
@writer_only(superuser=True)
def lect_delete(request, lect_no):
    lect = Lect.objects.get(pk=lect_no)

    if request.method == "POST":
        # 회장단에 의해 강의가 삭제된 경우 삭제된 강의에 대해 강의자에게 알림을 날림.
        cur_user = get_logined_user(request)
        if lect.lect_chief != cur_user and role_check(cur_user, 3, "lte"):
            delete_lect_by_superuser_alarm(request, lect)
        lect_type_no = lect.lect_type.type_no  # 강의 삭제 전 DB에 저장되어 있는 게시판 타입을 받아옴: 강의 리스트로 페이지를 리다이렉팅 하기 위함.
        FileController.delete_all_files_of_(lect)  # 강의에 저장되어 있는 사진 삭제
        for lect_board in lect.lectures.all():
            FileController.delete_all_files_of_(lect_board)
            comment_delete_by_post_delete(lect_board)
            lect_board.delete()
        lect.delete()  # 강의 DB에서 삭제
        return redirect("lect_view", type_no=lect_type_no)  # 강의 리스트로 페이지 전환
    return redirect("lect_detail", lect_no=lect.lect_no)


# 강의 리스트 이동 함수
@login_required
def lect_view(request, type_no):  # 게시판 페이지로 이동
    lect_list = get_page_object(request, get_lect_list(request, type_no))
    lect_type = get_lect_type(request, type_no)
    context = {
        "type": lect_type,
        "item_list": lect_list
    }
    return render(request, 'lecture_list.html', context)  # 정상 처리


# 게시글 검색 시 이동 함수
def lect_search(request, type_no):
    keyword = request.GET.get("keyword")
    lect_type = get_lect_type(request, type_no)
    # 기존 리스트에 검색 필터 추가 (검색 범위: 강의 제목, 강의 계획, 강의 소개)
    lect_list = get_page_object(request, get_lect_list(request, type_no).filter(
        Q(lect_intro__icontains=keyword) | Q(lect_title__icontains=keyword) | Q(
            lect_chief__user_name__icontains=keyword)), num_of_boards_in_one_page=9)
    lect_type.type_exp = "\"" + keyword + "\"(으)로 검색한 결과입니다."
    context = {
        "type": lect_type,
        "item_list": lect_list
    }
    return render(request, 'lecture_list.html', context)  # 정상 처리


# 유저 강의 명단 등록 함수
@prohibit_professor
@enroll_check
@ongoing_check
def lect_enroll(request, lect_no):
    cur_user = get_logined_user(request)
    if is_superuser(cur_user) and Lect.objects.get(pk=lect_no).lect_type_id == 1:
        return not_allowed(request, "운영진은 공정성을 위해, 강의 신청 권한이 없습니다.")
    else:
        messages.warning(request, "등록이 완료되었습니다.")
    lect_enrollment = LectEnrollment.objects.create(
        lect_no=Lect.objects.get(pk=lect_no),
        student=cur_user,
    )
    create_lect_enroll_alarm(lect_enrollment)
    create_lect_full_alarm(Lect.objects.get(pk=lect_no))
    # 강의실 메인 페이지로 리다이렉트
    return redirect('lect_room_main', room_no=lect_no)


# 과제 정보 가져오기 ( 과제게시글 더보기 / 내가 제출한 과제보기 / 강의실 메인 홈 )
def get_assignment_list(cur_user, lect_room, name_in_html):
    assignment_list = []

    # 강의자 : 글번호 / 과제글 / 제출된 수강생들의 과제 집계(총제출/총인원)
    if cur_user == lect_room.lect_chief:
        assignment_list = [{
            'idx': len(lect_room.lectures.filter(lect_board_type_id=3)) - idx,
            name_in_html: assignment,
            'status': str(len(assignment.submissions.all())) + '/' + str(len(lect_room.enrolled_students.all()))
        } for idx, assignment in enumerate(lect_room.lectures.filter(lect_board_type_id=3))]
    # 수강생 : 글번호 / 과제글 / 제출한 과제 현황.
    else:
        for idx, assignment in enumerate(lect_room.lectures.filter(lect_board_type_id=3)):
            status = LectAssignmentSubmit.objects.filter(assignment_no=assignment,
                                                         assignment_submitter=cur_user).first()
            assignment_list.append({
                'idx': len(lect_room.lectures.filter(lect_board_type_id=3)) - idx,
                name_in_html: assignment,
                'status': status.status.description if status else '미제출'})

    return assignment_list


# 강의룸 메인 페이지
@member_only(superuser=True)
@ongoing_check
def lect_room_main(request, room_no):
    try:
        lect_room = Lect.objects.prefetch_related('lectures', 'enrolled_students').get(pk=room_no)
    except Lect.DoesNotExist:
        messages.warning(request, "해당 강의를 찾을 수 없습니다. 삭제되었을 수 있습니다.")
        return redirect("lect_view", type_no=1)
    cur_user = get_logined_user(request)

    context = {
        'lect': lect_room,
        'notice_list': lect_room.lectures.filter(lect_board_type_id=1),  # 강의 공지글 불러오기
        'lect_board_list': lect_room.lectures.filter(lect_board_type_id=2),  # 강의 게시글 불러오기
        'assignment_list': get_assignment_list(cur_user, lect_room, name_in_html='assignment')  # 강의 과제 불러오기
    }
    return render(request, 'lecture_room_main.html', context)


@member_only()
@ongoing_check
def lect_room_search(request, room_no):
    if request.method == "GET":
        k = request.GET.get("keyword")

        search_result = LectBoard.objects.filter((Q(lect_board_title__icontains=k) | Q(lect_board_cont__icontains=k) |
                                                  Q(lect_board_writer__user_name__icontains=k)) & Q(
            lect_no_id=room_no)).order_by('-lect_board_created')

        # 검색 필터 (검색 범위: 강의게시글 제목, 강의게시글 내용, 강의게시글 작성자)
        board_list = get_page_object(
            request,
            model_list=[{'idx': len(search_result) - idx, 'board': board} for idx, board in enumerate(search_result)],
            num_of_boards_in_one_page=15)

        lect = Lect.objects.get(pk=room_no)
        lect.lect_intro = "\"" + k + "\"(으)로 검색한 결과입니다."

        context = {
            "lect": lect,
            "board_type": 0,
            "board_list": board_list,
            'searching': True  # lecture_room_board_list.html 를 재사용하기 때문에, url matching error 를 피하기 위함.
        }

        return render(request, 'lecture_room_board_list.html', context)  # 정상 처리

        # 강의 게시글 CRUD #


# 더보기 눌렀을 때 나오는 게시판 (공지게시판(1)/강의게시판(2)/과제게시판(3))
@member_only(superuser=True)
@ongoing_check
def lect_room_list(request, room_no, board_type):
    try:
        lect_room = Lect.objects.prefetch_related('enrolled_students', 'lectures', 'submitted_assignments').get(
            pk=room_no)
    except Lect.DoesNotExist:
        messages.warning(request, "해당 강의가 존재하지 않습니다. 삭제되었을 수 있습니다.")
        return redirect("lect_view", type_no=1)
    # 공지사항 및 강의게시판
    if board_type < 3:
        board_list = lect_room.lectures.filter(lect_board_type_id=board_type)
        board_list = [{'idx': len(board_list) - idx, 'board': board} for idx, board in enumerate(board_list)]
    # 과제게시판
    else:
        cur_user = get_logined_user(request)
        board_list = get_assignment_list(cur_user, lect_room, name_in_html='board')

    context = {
        'lect': lect_room,
        'board_list': get_page_object(request, board_list, 15),
        'board_type': board_type,
        'any_lecture': True if lect_room.lectures.filter(lect_board_type_id=2) else False  # 강의 x => 과제 작성 x
    }
    return render(request, 'lecture_room_board_list.html', context)


# 강의 게시글(공지/강의) 등록
@instructor_only()
@ongoing_check
def lect_board_register(request, room_no, board_type):
    if request.method == "GET":
        lect_room = Lect.objects.prefetch_related('lectures').get(pk=room_no)
        context = {
            'lect_board_form': make_lect_board_form(board_type),
            'file_form': FileForm(),
            'lect': lect_room,
            'lect_board_list': lect_room.lectures.filter(lect_board_type_id=2) if board_type == 3 else None,
            'board_type': board_type
        }
        # 게시글 등록 페이지로 이동!
        return render(request, 'lecture_room_board_register.html', context)

    elif request.method == "POST":
        lect_board_form = make_lect_board_form(board_type, request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if lect_board_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                lecture = lect_board_form.save(  # 공지 또는 강의 게시물 저장
                    lect_board_writer=get_logined_user(request),
                    lect_no=Lect.objects.get(pk=room_no),
                    lect_board_ref_id=request.POST.get('lect_board_ref')  # 과제글에 대한 셀프조인
                )
                file_form.save(instance=lecture)  # 공지 또는 강의 파일 저장

            return redirect('lect_board_detail', room_no=room_no, lect_board_no=lecture.pk)

        return redirect(request.path)


# 강의/공지 게시글 상세보기
@exist_check
@member_only(superuser=True)
@ongoing_check
def lect_board_detail(request, room_no, lect_board_no):
    lect_room = Lect.objects.get(pk=room_no)
    board = LectBoard.objects.get(pk=lect_board_no)
    files = board.files.all()
    link = board.lect_board_link
    file_list, img_list, doc_list = FileController.get_images_and_files_of_(board)
    # 과제 글
    submitted_assignment = None
    if board.lect_board_type_id == 3:
        # 수강생이면, 제출한 과제 보여주기
        cur_user = get_logined_user(request)
        if cur_user != lect_room.lect_chief:
            # 과제 하나당 수강생은 어차피 하나밖에 제출 못함. get 쿼리로 검사하면 레코드 없을 시 오류 발생.
            submitted_assignment = LectAssignmentSubmit.objects.filter(assignment_submitter=cur_user,
                                                                       assignment_no=board).first()

    # 강의 링크가 있으면 임베딩 시도
    link_embedding = {}
    if board.lect_board_type_id == 2 and link:
        if is_youtube(link):
            link_embedding['youtube'] = get_youtube(link)
        else:
            link_embedding['og'] = get_og_tag(link)

    code = {'code_files': []}
    for file in files:
        if FileController.is_code_file(file.file_name):
            code['code_files'].append({'file_name': file.file_name,
                                       'code': FileController.get_code_in_file(file.file_path.path)})

    context = {
        'lect': lect_room,
        'board': board,
        'doc_list': file_list,
        'submitted_assignment': submitted_assignment,
    }
    context.update(link_embedding)
    context.update(code)
    return render(request, 'lecture_room_board_detail.html', context)


# 강의/공지 게시글 삭제
@writer_only()
def lect_board_delete(request, room_no, lect_board_no):
    lect_board = get_object_or_404(LectBoard, pk=lect_board_no)

    FileController.delete_all_files_of_(lect_board)
    comment_delete_by_post_delete(lect_board)
    lect_board.delete()

    return redirect('lect_room_main', room_no=room_no)


# 강의/공지 게시글 수정
@instructor_only()
def lect_board_update(request, room_no, lect_board_no):
    board = LectBoard.objects.prefetch_related('files').get(pk=lect_board_no)
    board_type = board.lect_board_type_id

    if request.method == "GET":
        context = {
            'lect': Lect.objects.get(pk=room_no),
            'lect_board_form': make_lect_board_form(board_type, instance=board),  # 강의/공지 폼
            'file_form': FileForm(),  # 강의 파일 폼
            'board_no': lect_board_no,
            'board_type': board_type,
            'file_list': board.files.all(),  # 게시글 기존 파일 리스트
            'lect_board_list': LectBoard.objects.filter(lect_no_id=room_no, lect_board_type_id=2
                                                        ) if board_type == 3 else None,  # 과제글의 경우 상단 select 박스
            'lect_board_ref': board.lect_board_ref_id if board_type == 3 else None  # 과제글의 경우 부모 게시글

        }
        return render(request, 'lecture_room_board_register.html', context)

    elif request.method == "POST":
        lect_board_form = make_lect_board_form(board_type, request.POST)  # 강의/공지 폼
        file_form = FileForm(request.POST, request.FILES)  # 강의 파일 폼

        if lect_board_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                if board_type == 3:  # 과제글의 경우
                    board.lect_board_ref = get_object_or_404(LectBoard, pk=request.POST.get("lect_board_ref"))
                lect_board_form.update(instance=board)
                FileController.remove_files_by_user(request, board.files.all())
                file_form.save(instance=board)

        return redirect('lect_board_detail', room_no=room_no, lect_board_no=lect_board_no)

        # 수강생 과제 CRUD #


# 수강생 과제 제출
@member_only()
@ongoing_check
def lect_assignment_submit(request, room_no):
    lect_room = get_object_or_404(Lect, lect_no=room_no)

    if request.method == "GET":
        assignment = LectBoard.objects.get(pk=request.GET.get('lect_board_no'))
        context = {
            'lect': lect_room,
            'assignment_form': AssignmentSubmitForm(initial={'assignment_title': assignment.lect_board_title}),
            'file_form': FileForm(),
            'assignment': assignment
        }
        return render(request, 'lecture_assignment_submit.html', context)

    elif request.method == "POST":
        submit_form = AssignmentSubmitForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if submit_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                submission = submit_form.save(
                    lect_board_no=request.POST.get('lect_board_no'),
                    assignment_submitter=get_logined_user(request),
                    lect_no=room_no
                )
                file_form.save(instance=submission)

        return redirect(reverse('lect_assignment_detail', args=[room_no, submission.pk]))


# 제출한 과제 목록
@member_only()
@ongoing_check
def lect_assignment_list(request, room_no):
    lect_room = Lect.objects.prefetch_related('submitted_assignments').get(pk=room_no)
    cur_user = get_logined_user(request)
    assignments_list = get_page_object(
        request,
        model_list=lect_room.submitted_assignments.select_related('assignment_no').filter(
            assignment_submitter=cur_user).all(),
        num_of_boards_in_one_page=15)

    context = {
        'lect': lect_room,
        'assignments_list': assignments_list,
    }

    return render(request, 'lecture_room_board_list.html', context)


# 수강생이, 제출한 과제 수정
@writer_only()
@ongoing_check
def lect_assignment_update(request, room_no, submit_no):
    lect_room = get_object_or_404(Lect, pk=room_no)
    submitted_assignment = LectAssignmentSubmit.objects.prefetch_related('files').get(pk=submit_no)

    if request.method == "GET":
        context = {
            'lect': lect_room,
            'assignment_form': AssignmentSubmitForm(instance=submitted_assignment),
            'submitted_assignment': submitted_assignment,
            'assignment': submitted_assignment.assignment_no,
            'file_form': FileForm(),
            'file_list': submitted_assignment.files.all()
        }
        return render(request, 'lecture_assignment_submit.html', context)

    elif request.method == "POST":
        assignment_form = AssignmentSubmitForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if assignment_form.is_valid() and file_form.is_valid():
            assignment_form.update(submitted_assignment)
            FileController.remove_files_by_user(request, submitted_assignment.files.all())
            file_form.save(instance=submitted_assignment)

        return redirect(reverse('lect_assignment_detail', args=[room_no, submit_no]))


# 수강생이, 제출했던 과제 삭제하는 경우
@writer_only()
def lect_assignment_delete(request, room_no, submit_no):
    if request.method == "POST":
        assignment = get_object_or_404(LectAssignmentSubmit, pk=submit_no)
        FileController.delete_all_files_of_(assignment)
        assignment.delete()

    return redirect(reverse('lect_assignment_list', args=[room_no]))

    # 수강생 메뉴 #


# 제출한 과제 보기/ 강의자와 운영팀도 접근 가능
@writer_only(is_lect_assignment=True)
@ongoing_check
def lect_assignment_detail(request, room_no, submit_no):
    lect_room = get_object_or_404(Lect, pk=room_no)
    submitted_assignment = LectAssignmentSubmit.objects.prefetch_related('files').select_related('assignment_no').get(
        pk=submit_no)
    file_list, img_list, doc_list = FileController.get_images_and_files_of_(submitted_assignment)

    if request.method == "GET":
        context = {
            'lect': lect_room,
            'submitted_assignment': submitted_assignment,
            'file_list': file_list,
            'img_list': img_list,
            'doc_list': doc_list,
        }

        return render(request, "lecture_assignment_detail.html", context)


# 수강생이 자신의 출결과 과제제출 현황 보는 곳
@member_only()
def lect_room_student_status(request, room_no):
    lect_room = Lect.objects.prefetch_related("lectures", "attendance").get(pk=room_no)
    lect_board_list = lect_room.lectures.prefetch_related('assignments').filter(lect_board_type_id=2  # 강의 게시글들
                                                                                ).order_by('lect_board_created')
    cur_user = get_logined_user(request)
    attend_info = LectAttendance.objects.filter(lect_no=lect_room, student=cur_user)  # 현재 유저의 출석
    lect_board_list = [{
        'idx': idx + 1,  # 회차
        'lecture': lect_board,
        'attend': '출석' if attend_info.filter(lect_board_no=lect_board) else '결석',
        'assignments': [{
            'assignment': assignment,
            'submission': LectAssignmentSubmit.objects.filter(assignment_submitter=cur_user,
                                                              assignment_no=assignment).first()
        } for assignment in lect_board.assignments.all()]
    } for idx, lect_board in enumerate(lect_board_list)
    ]

    context = {
        'lect': lect_room,
        'lect_board_list': lect_board_list,
        'item_list': get_page_object(request, lect_board_list, 10),
    }

    return render(request, 'lecture_room_student_status.html', context)


def lect_room_exit(request, room_no):
    cur_student = LectEnrollment.objects.prefetch_related('lect_no').get(
        lect_no=room_no, student_id=request.session.get('user_stu'))
    cur_student.status_id = -1
    cur_student.exit_time = today()
    cur_student.save()

    create_user_lect_out_alarm(lect_enrollment=cur_student)

    return redirect('lect_view', type_no=1)

    # 강의자 메뉴 #


# 강의자가 수강생의 과제 디테일 조회 시, 수강생의 과제를 통과 또는 실패 처리 시킴
@instructor_only()
def lect_assignment_aor(request, room_no, submit_no):
    if request.method == "POST":
        aor = int(request.POST.get('aor'))
        submitted_assignment = get_object_or_404(LectAssignmentSubmit, pk=submit_no)

        # 과제 통과 or 거절 시키겠음!
        if aor == 1 or aor == -1:
            submitted_assignment.status_id = aor
            submitted_assignment.reject_reason = request.POST.get("reject_reason")
            submitted_assignment.save()

        return redirect(reverse('lect_assignment_detail', args=[room_no, submit_no]))


# 강의자가 수강생 수강정지 시킬 수 있는 곳.
# 수강생들의 출석정보를 한 눈에 볼 수 있음. 운영팀은 GET 만 접근 가능
@instructor_only(superuser=True)
def lect_room_manage_member(request, room_no):
    lect_room = Lect.objects.prefetch_related('lectures', 'attendance', 'submitted_assignments',
                                              'lectures__assignments').get(pk=room_no)
    lectures = lect_room.lectures.filter(lect_board_type_id=2)

    if request.method == "GET":
        # 출석 정보 알아내기
        lect_attend_info = lect_room.attendance.filter(lect_no_id=room_no)  # 해당 강의에 속한 모든 수강생의 출석 정보
        assignment_info = lect_room.submitted_assignments  # 제출된 모든 수강생의 과제
        students = list(
            LectEnrollment.objects.prefetch_related('student__useremail_set').filter(lect_no_id=room_no))  # 수강생 명단
        total_attend_info = [len(lect_attend_info.filter(student=stu.student)) for stu in students]  # 개인별 출석 횟수
        attend_info_list = [{
            'enrolled': stu,
            'attend': attend,
            'assignment_info': str(len(assignment_info.filter(assignment_submitter=stu.student)))  # 수강생 별 과제 제출 수
                               + '/' + str(len(lect_room.lectures.filter(lect_board_type_id=3)))  # 총 과제
        } for stu, attend in zip(students, total_attend_info)]  # 하나의 딕셔너리로 묶기

        context = {
            'attend_info_list': attend_info_list,  # 출석 정보 알아내기
            'lect': Lect.objects.get(pk=room_no),
            'item_list': get_page_object(request, students, 15),  # 15 명씩 보이게 출력
            'total_check': len(lectures)
        }

        return render(request, 'lecture_room_manage_students.html', context)

    elif request.method == "POST":
        if request.POST.get('status_mode') in ['0', '1']:
            status_mode = int(request.POST.get('status_mode'))
            checked_list = [request.POST[key] for key in request.POST if 'is_checked_' in key]  # 체크된 수강생들 pk 값 받아오기
            students = LectEnrollment.objects.filter(pk__in=checked_list)  # 체크된 수강생들 쿼리 ORM

            for std in students:
                std.status_id = status_mode

            LectEnrollment.objects.bulk_update(
                objs=students, fields=['status', ]
            )

        return redirect(reverse('lect_room_manage_member', args=[room_no]))


# 과제 현황 조회
# 운영팀은 GET 만 접근 가능
@instructor_only(superuser=True)
@ongoing_check
def lect_room_manage_assignment(request, room_no):
    if request.method == "GET":
        lect_room = Lect.objects.prefetch_related(
            "lectures", "enrolled_students", "submitted_assignments", "submitted_assignments__files").get(pk=room_no)

        any_assignment = lect_room.lectures.filter(lect_board_type_id=3).first()
        # 과제 게시글 번호. select option 값 / default 는 마지막 강의 게시글
        # 처음 이 페이지를 렌더링 할 때는 get 파라미터가 존재하지 않음. 이 강의 첫 게시글이 존재하지 않으면, 게시글 번호 존재 X
        assignment_no = request.GET.get('assignment_no',
                                        None if not any_assignment else any_assignment.lect_board_no)

        students_list = lect_room.enrolled_students.all()
        if any_assignment and students_list:
            students_list = [{
                'student': std.student,
                'exit_time': std.exit_time,
                'submission': lect_room.submitted_assignments.filter(  # 제출시간, 제출여부, 제출된 파일에 접근하기 위한 객체
                    assignment_submitter=std.student, assignment_no=assignment_no).first()
            } for std in students_list]

        context = {
            'lect': lect_room,
            'cur_assignment': None if assignment_no is None else LectBoard.objects.get(pk=assignment_no),
            'students_list': students_list,
            'lect_board_list': lect_room.lectures.filter(lect_board_type_id=2),
        }

        return render(request, 'lecture_room_manage_assignment.html', context)

    elif request.method == "POST":
        manage_mode = int(request.POST.get('manage_mode'))
        if manage_mode in [-1, 1]:
            checked_list = [request.POST[key] for key in request.POST if 'is_checked_' in key and request.POST[key]]
            assignments = LectAssignmentSubmit.objects.filter(pk__in=checked_list)
            for s in assignments:
                s.status_id = manage_mode

            LectAssignmentSubmit.objects.bulk_update(objs=assignments, fields=['status', ])

            return redirect(reverse('lect_room_manage_assignment', args=[room_no]))

        else:
            # 잘못된 경우
            return redirect(reverse('lect_room_main', args=[room_no]))


# 출석 현황 확인 및 변경
# 강의 게시글이 존재하지 않으면 => 출석부 ('_table_attendance_check.html') 렌더하지 않음.
# 강의 게시글은 존재하지만, 학생이 없으면 => 출석부 렌더하지만, 학생이 아무도 없음.
# 운영팀은 GET 만 접근 가능
@instructor_only(superuser=True)
@ongoing_check
def lect_room_manage_attendance(request, room_no):
    lect_room = Lect.objects.prefetch_related("lectures", "enrolled_students__student").get(pk=room_no)
    lect_board_list = lect_room.lectures.filter(lect_board_type_id=2).order_by('-lect_board_no')  # 강의 게시글만 가져옴

    if request.method == "GET":
        # 강의 게시글 번호. select option 값 / default 는 마지막 강의 게시글
        # 처음 이 페이지를 렌더링 할 때는 get 파라미터가 존재하지 않음. 이 강의 첫 게시글이 존재하지 않으면, 게시글 번호 존재 X
        lect_board_no = request.GET.get('lect_board_no',
                                        None if not lect_board_list else lect_board_list[0].lect_board_no)

        # 강의 게시물이 있고, 수강생이 있는 두 경우를 모두 충족시켜야 출석페이지 출력가능
        students_list = lect_room.enrolled_students.all()
        if lect_board_list and students_list:
            # 장고 ORM 으로 쿼리 수행 불가하여, raw query 작성.
            # connection : default db에 연결되어 있는 built in 객체
            # (on 부분) enrollment.STUDENT 가 없으면 mariadb 오류!
            query = f"""
                    SELECT 
                        u.USER_NAME, 
                        u.USER_STU, 
                        MAJOR_INFO.MAJOR_NAME, 
                        enrollment.exit_time,
                        if(isnull(attend.LECT_ATTEND_DATE),false,true) as attendance
                    FROM LECT_ENROLLMENT AS enrollment

                    LEFT OUTER JOIN 
                        LECT_ATTENDANCE AS attend 
                        on (enrollment.STUDENT = attend.STUDENT AND attend.LECT_BOARD_NO = {lect_board_no})

                    INNER JOIN 
                        USER as u ON (enrollment.STUDENT = u.USER_STU),
                        MAJOR_INFO

                    WHERE 
                        enrollment.LECT_NO = {lect_room.lect_no} 
                        and u.USER_MAJOR = MAJOR_INFO.MAJOR_NO

                    ORDER BY u.USER_NAME ;"""
            cursor = connection.cursor()
            cursor.execute(query)  # 쿼리 수행
            students_list = [{
                'index': index + 1,
                'name': name,
                'stu': stu,
                'major': major,
                'exit_time': exit_time,
                'attendance': '출석' if attendance == 1 else '결석'
            } for index, (name, stu, major, exit_time, attendance) in enumerate(cursor.fetchall())]

        context = {
            'lect': lect_room,
            'lect_board_list': lect_board_list,
            'cur_lect_board': None if lect_board_no is None else LectBoard.objects.get(pk=lect_board_no),  # 현재 게시글
            'students_list': get_page_object(request, students_list, 15),  # 15 명씩 보이게 출력
        }
        return render(request, 'lecture_room_manage_attendance.html', context)

    elif request.method == "POST":
        lect_board = LectBoard.objects.get(pk=request.POST.get('lect_board_no_'))
        manage_mode = {'출석': True, '결석': False} if request.POST.get('manage-mode') == '1' else {'결석': True, '출석': False}
        checked_list = [request.POST[key] for key in request.POST if 'is_checked_' in key]  # 체크된 수강생들

        if lect_board is not None:
            if manage_mode['출석']:
                # input checkbox 로 넘어온 모든 학번에 대해, 출석처리
                # db 에서 (게시글 번호, 학번) 묶어서 unique key 설정했음.
                LectAttendance.objects.bulk_create([
                    LectAttendance(lect_no_id=room_no, lect_board_no=lect_board, student_id=stu) for stu in checked_list
                    if not LectAttendance.objects.filter(lect_board_no=lect_board, student_id=stu)  # 이미 출석된 상태가 아니면,
                ])
            elif manage_mode['결석']:
                # input checkbox 로 넘어온 모든 학번에 대해, 결석처리
                # db에 수강생의 레코드가 존재하지 않는 경우 결석이라고 해석하고 있기 때문에 filter 로 쿼리 불러야함.
                # 이미 결석인 수강생에 대해 중복 결석 처리했을 때, get 을 사용하면 에러발생.
                students = LectAttendance.objects.filter(lect_board_no=lect_board)
                students.filter(student_id__in=checked_list).delete()

        return redirect(reverse('lect_room_manage_attendance', kwargs={'room_no': room_no}), )


# 제작: 양태영
# 제작일: 2021-08-11
# 설명: 강의자가 강의를 종강처리할 때 사용하는 뷰.
@instructor_only(superuser=False)  # 강의자만 가능, 관리자는 임의로 종강 처리할 수 없음.
def lect_terminate(request, lect_no):
    lect = Lect.objects.get(pk=lect_no)
    lect.lect_state = StateInfo.objects.get(pk=4)
    lect.save()
    # 종강 처리 정상처리 이후 메시지를 띄움.
    messages.warning(request, "정상적으로 종강 처리되었습니다. IBAS에서 강의해주셔서 정말 감사합니다.")
    return redirect("lect_view", type_no=lect.lect_type_id)
