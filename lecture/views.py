from django.db import transaction, connection
from django.sh
ortcuts import render, redirect, reverse, get_object_or_404
from DB.models import LectType, Lect, LectDay, StateInfo, MethodInfo, LectBoard, LectBoardFile, \
    LectAssignment, LectEnrollment, LectAttendance
from django.db.models import Q
from pagination_handler import get_paginator_list, get_page_object
from lecture.forms import LectForm, LectRejectForm, LectPicForm, LectBoardForm, make_lect_board_form, \
    LectAssignmentForm, FileForm, AssignmentFileForm
from user_controller import get_logined_user, login_required, superuser_only, writer_only, auth_check, is_superuser, \
    is_logined
from file_controller import FileController
from django.utils.dateformat import DateFormat


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
        lect_type = LectType.objects.get(pk=type_no)
        lect_list = Lect.objects.filter(Q(lect_type=lect_type) & Q(lect_state__state_no=3)).prefetch_related(
            "lectday_set", "enrolled_students")
    else:
        lect_list = Lect.objects.filter(Q(lect_type=LectType.objects.get(pk=1)) & Q(lect_state__state_no=1) | Q(
            lect_state__state_no=2)).prefetch_related("lectday_set").prefetch_related("lectuser_set")
    return lect_list


# 타입에 맞는 강의 타입 인스턴스를 반환하는 함수
def get_lect_type(request, type_no):
    if type_no != 4:
        lect_type = LectType.objects.get(pk=type_no)
    else:
        if not is_logined(request) or not is_superuser(request):  # 강의 개설 관련 처리는 관리자만 할 수 있으므로 관리자 권한 체크
            return redirect(reverse("index"))
        lect_type = LectType()
        lect_type.type_no = type_no
        lect_type.type_no = 4
        lect_type.type_name = "강의 개설 신청"
        lect_type.type_exp = "개설 신청된 강의 목록입니다."
    return lect_type


# Create your views here.
@auth_check(active=True)
def lect_register(request):  # 강의/스터디/취미모임 등록 페이지로 이동하는 것
    if request.method == "GET":
        lect_type = LectType.objects.get(pk=request.GET.get("lect_type"))
        init_dict = {"lect_type": lect_type.type_no}
        if lect_type.type_no == 1:  # 강의일 때
            init_dict.update(lect_state=1)
        else:  # 강의가 아닐 때
            init_dict.update(lect_state=3)
        context = {
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
            return redirect("lect_detail", lect_no=lect.lect_no)
        else:  # 유효성 검사 실패 시
            return redirect("lect_view", type_no=1)


# 강의 상세 페이지로 이동 (활동 회원만 가능)
@auth_check(active=True)
def lect_detail(request, lect_no):
    lect = Lect.objects.get(pk=lect_no)
    lect_day_list = LectDay.objects.filter(lect_no=lect_no)
    context = {
        'lect': lect,
        'lect_day_list': lect_day_list,
        'lect_user_num': LectEnrollment.objects.filter(lect_no=lect_no).count(),
        'is_in': LectEnrollment.objects.filter(student=get_logined_user(request), lect_no__lect_no=lect_no) is not None,
        'lect_reject_form': LectRejectForm(instance=lect),
    }
    # 취미 모임의 경우 강의 방식이 없음 따라서 해당 부분에 대한 예외처리
    if lect.lect_method is not None:
        context.update(pol_name=get_pol_name(lect.lect_method.method_no))
    return render(request, 'lecture_detail.html', context)


@superuser_only
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
        if lect_form.is_valid() and lect_pic_form.is_valid():
            lect_form.update(instance=lect)
            if lect_pic_form.has_changed():
                FileController.delete_all_files_of_(lect)
                lect_pic_form.save(instance=lect)
        return redirect("lect_detail", lect_no=lect.lect_no)
    else:  # 상세 페이지에서 수정 버튼을 눌렀을 때
        context = {
            "lect_type": lect.lect_type,
            "method_list": MethodInfo.objects.all(),
            "lect_form": LectForm(instance=lect),
            "lect_pic_form": LectPicForm(instance=lect),
            "is_update": True,
            "lect_no": lect.lect_no,
        }
        if lect.lect_method is not None:
            context.update(pol_name=get_pol_name(lect.lect_method.method_no))
        return render(request, "lecture_register.html", context)


# 강의 삭제 함수
@writer_only(superuser=True)
def lect_delete(request, lect_no):
    lect = Lect.objects.get(pk=lect_no)
    if request.method == "POST":
        lect_type_no = lect.lect_type.type_no  # 강의 삭제 전 DB에 저장되어 있는 게시판 타입을 받아옴: 강의 리스트로 페이지를 리다이렉팅 하기 위함.
        FileController.delete_all_files_of_(lect)  # 강의에 저장되어 있는 사진 삭제
        lect.delete()  # 강의 DB에서 삭제
        return redirect("lect_view", type_no=lect_type_no)  # 강의 리스트로 페이지 전환
    return redirect("lect_detail", lect_no=lect.lect_no)


# 강의 리스트 이동 함수
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
def lect_enroll(request, lect_no):
    LectEnrollment.objects.create(
        lect_no=Lect.objects.get(pk=lect_no),
        student=get_logined_user(request),
        )

    # 강의실 메인 페이지로 리다이렉트
    return redirect('lect_room_main', room_no=lect_no)


# 강의룸 메인 페이지
def lect_room_main(request, room_no):
    context = {
        'lect': Lect.objects.get(pk=room_no),
        'notice_list': LectBoard.objects.filter(lect_board_type__lect_board_type_no=1  # 강의 공지글 불러오기
                                                ).order_by('-lect_board_created'),
        'lect_board_list': LectBoard.objects.filter(lect_board_type__lect_board_type_no=2  # 강의 게시글 불러오기
                                                    ).order_by('-lect_board_created'),
        'assignment_list': LectAssignment.objects.filter(lect_board_no__lect_no__lect_no=room_no  # 이 강의에 속한 과제 불러오기
                                                         ).order_by('-lect_assignment_created'),
    }
    return render(request, 'lecture_room_main.html', context)


# 더보기 눌렀을 때 나오는 게시판 (공지게시판(1)/강의게시판(2)/과제게시판(3))
def lect_room_list(request, room_no, board_type):
    if board_type == 3:
        board_list = LectAssignment.objects.filter(lect_board_no__lect_no__lect_no=room_no).order_by('-lect_assignment_created')
    else:
        board_list = LectBoard.objects.filter(lect_board_type__lect_board_type_no=board_type).order_by('-lect_board_created')

    page_obj = get_page_object(request, board_list, 15)  # 페이지네이션 15개 글이 한 페이지

    context = {
        'lect': Lect.objects.get(pk=room_no),
        'board_list': board_list,
        'board_type': board_type,
        'item_list': page_obj
    }
    return render(request, 'lecture_room_list.html', context)


# 강의 게시글(공지/강의) 등록
def lect_board_register(request, room_no, board_type):
    if request.method == "GET":
        context = {
            'lect_board_form': make_lect_board_form(board_type),
            'file_form': FileForm(),
            'assignment_file_form': AssignmentFileForm() if board_type == 2 else None,  # 강의게시글에만 과제 존재
            'assignment_form': LectAssignmentForm(initial={'board_type': 3}) if board_type == 2 else None,
            'lect': Lect.objects.get(pk=room_no),
            'board_type': board_type
        }
        # 게시글 등록 페이지로 이동!
        return render(request, 'lecture_room_board_register.html', context)

    elif request.method == "POST":
        lect_board_form = make_lect_board_form(board_type, request.POST)
        file_form = FileForm(request.POST, request.FILES)
        assignment_form = LectAssignmentForm(request.POST)  # 강의게시글에만 과제 존재 (공지게시글에는 존재 x)
        assignment_file_form = AssignmentFileForm(request.POST, request.FILES)  # 강의게시글에만 과제 존재 (공지게시글에는 존재 x)
        has_assignment = bool(request.POST.get('has_assignment'))  # '과제가 있습니다' 체크박스 value 값

        if lect_board_form.is_valid() and file_form.is_valid():
            # 트렌젝션 꼭 보장되어야함!
            with transaction.atomic():
                lecture = lect_board_form.save(  # 공지 또는 강의 게시물 저장
                    lect_board_writer=get_logined_user(request),
                    lect_no=Lect.objects.get(pk=room_no),
                )
                file_form.save(instance=lecture)  # 공지 또는 강의 파일 저장

                # 과제가 있을 때
                if has_assignment and assignment_form.is_valid() and assignment_file_form.is_valid():
                    assignment = assignment_form.save(  # 과제 게시글 저장
                        lect_board_writer=lecture.lect_board_writer,
                        lect_board_no=lecture,
                    )
                    assignment_file_form.save(instance=assignment)  # 과제 파일 저장

        return redirect('lect_room_main', room_no=room_no)


# 강의/공지 게시글 상세보기
def lect_board_detail(request, room_no, board_no):
    board = get_object_or_404(LectBoard, pk=board_no)
    file_list, img_list, doc_list = FileController.get_images_and_files_of_(board)

    context = {
        'lect': get_object_or_404(Lect, pk=room_no),
        'board': board,
        'file_list': file_list,
        'img_list': img_list,
        'doc_list': doc_list
    }
    return render(request, 'lecture_room_board_detail.html', context)


# 강의/공지 게시글 삭제
def lect_board_delete(request, room_no, board_no):
    lect_board = get_object_or_404(LectBoard, pk=board_no)

    FileController.delete_all_files_of_(lect_board)
    lect_board.delete()

    return redirect('lect_room_main', room_no=room_no)


# 강의/공지 게시글 수정
def lect_board_update(request, room_no, board_no):
    board = LectBoard.objects.prefetch_related('file', 'assignment', 'assignment__file').get(pk=board_no)
    assignment = board.assignment.first()  # 공지 => None, 강의 => 해당 과제
    board_type = board.lect_board_type_no.lect_board_type_no

    if request.method == "GET":
        context = {
            'lect': Lect.objects.get(pk=room_no),
            'lect_board_form': make_lect_board_form(board_type, instance=board),  # 강의/공지 폼
            'file_form': FileForm(),  # 강의 파일 폼
            'assignment_form': LectAssignmentForm(instance=assignment),  # 과제 게시글 폼
            'assignment_file_form': AssignmentFileForm(),  # 과제 파일 폼
            'board_no': board_no,
            'board_type': board_type,
            'file_list': board.file.all(),  # 게시글 기존 파일 리스트
            'assignment_file_list': assignment.file.all() if assignment is not None else None  # 과제 기존 파일 리스트
        }
        return render(request, 'lecture_room_board_register.html', context)

    elif request.method == "POST":
        lect_board_form = make_lect_board_form(board_type, request.POST)  # 강의/공지 폼
        file_form = FileForm(request.POST, request.FILES)  # 강의 파일 폼
        assignment_form = LectAssignmentForm(request.POST)  # 과제 폼
        assignment_file_form = AssignmentFileForm(request.POST, request.FILES)  # 과제 파일 폼
        has_assignment = bool(request.POST.get('has_assignment'))  # '과제가 있습니다' 체크박스 value 값

        if lect_board_form.is_valid() and file_form.is_valid():
            # 트랜젝션 꼭 있어야 함!
            with transaction.atomic():
                lect_board_form.update(instance=board)
                FileController.remove_files_by_user(request, board.file.all())
                file_form.save(instance=board)
                if has_assignment and assignment_form.is_valid() and assignment_file_form.is_valid():
                    # 과제가 기존에 없었으면 생성, 있었으면 수정!
                    if assignment is not None:
                        assignment_form.update(instance=assignment)
                    else:
                        assignment = assignment_form.save(
                            lect_board_writer=board.lect_board_writer,
                            lect_no=board.lect_no,
                            lect_board_ref=board,
                        )
                    FileController.remove_files_by_user(request, assignment.file.all())
                    assignment_file_form.save(instance=assignment)

        return redirect('lect_board_detail', room_no=room_no, board_no=board_no)


def lect_room_mem_manage(request, room_no):
    students = LectEnrollment.objects.filter(lect_no__lect_no=room_no)

    context = {
        'students': students,
        'lect': Lect.objects.get(pk=room_no),
        'item_list': get_page_object(request, students, 15)  # 15 명씩 보이게 출력
    }

    return render(request, 'lecture_room_mem_manage.html', context)


def lect_room_attend_std(request, room_no):
    lect_room = Lect.objects.prefetch_related("lectures").get(pk=room_no)

    context = {
        'lect': lect_room,
        'lect_board_list': lect_room.lectures
    }

    return render(request, 'lecture_room_attend_std.html', context)


# 출석 현황 확인 및 변경
def lect_room_attend_teacher(request, room_no):
    lect_room = Lect.objects.prefetch_related("lectures", "enrolled_students__student").get(pk=room_no)
    lect_board_list = lect_room.lectures.filter(lect_board_type_id=2).order_by('-lect_board_no')  # 강의 게시글만 가져옴

    # 강의 게시글 번호. select option 값 / default 는 마지막 강의 게시글, 게시글이 하나도 없으면 0.

    if request.method == "GET":
        # 처음 이 페이지를 렌더링 할 때는 get 파라미터가 존재하지 않음. 이 강의 첫 게시글이 존재하지 않으면, 게시글 번호 존재 X
        lect_board_no = request.GET.get('lect_board_no',
                                        None if lect_board_list[0] is None else lect_board_list[0].lect_board_no)

        # 장고 ORM 으로 쿼리 수행 불가하여, raw query 작성.
        # connection : default db에 연결되어 있는 built in 객체
        query = f"""SELECT u.USER_NAME, u.USER_STU, if(isnull(attend.LECT_ATTEND_DATE),false,true) as attendance
                FROM LECT_ENROLLMENT AS enrollment
    
                LEFT OUTER JOIN LECT_ATTENDANCE AS attend
                on (enrollment.STUDENT = attend.STUDENT AND attend.LECT_BOARD_NO = {lect_board_no})
    
                INNER JOIN USER as u
                ON (enrollment.STUDENT = u.USER_STU)
    
                WHERE enrollment.LECT_NO = {room_no}
    
                ORDER BY u.USER_NAME ASC;"""
        cursor = connection.cursor()
        cursor.execute(query)  # 쿼리 수행
        students_list = [{'name': name, 'stu': stu, 'attendance': '출석' if attendance == 1 else '결석'}
                         for name, stu, attendance in cursor.fetchall()]  # 쿼리 반환 값을 템플릿에서 사용할 수 있게, dict 로 변환

        context = {
            'lect': lect_room,
            'lect_board_list': lect_board_list,
            'students_list': students_list,  # 이름/학번/출석결석
            'cur_lect_board': None if lect_board_no is None else LectBoard.objects.get(pk=lect_board_no),  # 현재 게시글
            'item_list': get_page_object(request, students_list, 15) # 15 명씩 보이게 출력
        }
        return render(request, 'lecture_room_attend_teacher.html', context)

    elif request.method == "POST":
        lect_board = LectBoard.objects.get(pk=request.POST.get('lect_board_no_'))
        manage_mode = {'출석': True, '결석': False} if request.POST.get('manage-mode') == '1' else {'결석': True, '출석': False}
        checked_list = [request.POST[key] for key in request.POST if 'is_checked_' in key]

        if lect_board is not None:
            if manage_mode['출석']:
                # input checkbox 로 넘어온 모든 학번에 대해, 출석처리
                # db 에서 (게시글 번호, 학번) 묶어서 unique key 설정했음.
                for stu in checked_list:
                    LectAttendance.objects.create(lect_board_no=lect_board, student_id=stu)
            elif manage_mode['결석']:
                # input checkbox 로 넘어온 모든 학번에 대해, 결석처리
                # db에 수강생의 레코드가 존재하지 않는 경우 결석이라고 해석하고 있기 때문에 filter 로 쿼리 불러야함.
                # 이미 결석인 수강생에 대해 중복 결석 처리했을 때, get 을 사용하면 에러발생.
                for stu in checked_list:
                    LectAttendance.objects.filter(lect_board_no=lect_board, student_id=stu).delete()

        return redirect(reverse('lect_room_attend_teacher', kwargs={'room_no': room_no}))


def lect_board_hw_register(request):  # 강의룸 등록 페이지로 이동
    return render(request, 'lect_board_hw_register.html', {})



