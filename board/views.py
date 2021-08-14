from django.db import transaction
from django.shortcuts import render, redirect, reverse, get_object_or_404
from DB.models import Board, BoardFile, BoardType, ContestBoard, ContestFile
from django.db.models import Q
from board.forms import BoardForm, ContestForm, FileForm
from file_controller import FileController
from pagination_handler import get_page_object
from alarm.alarm_controller import create_board_notice_alarm, delete_board_by_superuser_alarm
from user_controller import login_required, writer_only, auth_check, get_logined_user, not_allowed, role_check, \
    superuser_only
from django.contrib import messages
from date_controller import today_after_day, today_after_year, today
from exception_handler import exist_check
from post_controller import comment_delete_by_post_delete


# 상단 기준일을 가지고 오는 함수
def get_fixdate(request):
    is_board_fixed = request.POST.get("board_fixdate")
    board_fixdate = None
    if is_board_fixed == "2weeks":
        board_fixdate = today_after_day(14)
    elif is_board_fixed == "permanent":
        board_fixdate = today_after_year(100)
    return board_fixdate


# 등록 버튼을 표시할 지, 말지 고르는 함수
def is_register_btn_show(request, board_type_no):
    cur_user = get_logined_user(request)
    auth_no = cur_user.user_auth.auth_no

    if board_type_no == 1:  # 공지사항
        if role_check(cur_user, 5, "lte"):  # 회장단 or 교수인가?
            return True
    elif board_type_no < 5:  # 자유게시판, 질문게시판, 활동게시판
        if auth_no != 3:  # 미승인 회원이 아닌가
            return True
    elif 6 <= board_type_no <= 7:
        if auth_no == 1 and not role_check(cur_user, 5, "equal"):  # 활동 회원이면서 교수가 아닌가?
            return True
    elif board_type_no == 8:  # 회장단 게시판
        if role_check(cur_user, 4, "lte"):  # 회장단인가
            return True
    elif board_type_no == 9:  # 건의 게시판
        if auth_no != 3:  # 미승인 회원이 아닌가
            return True
    return False

    # ---- get_sidebar_information ---- #


# INPUT : Board 객체 or ContestBoard 객체
# OUTPUT : 없음
# RETURN : dict Type / 각 게시판의 게시글 수
# 작성자 : 유동현
# 마지막 수정 일시 : 2021.04.13
def get_sidebar_information():
    return {
        "all_num": Board.objects.filter(board_type_no__board_type_no__lte=4).count(),
        "notice_num": Board.objects.filter(board_type_no__board_type_no=1).count(),
        "free_num": Board.objects.filter(board_type_no__board_type_no=2).count(),
        "quest_num": Board.objects.filter(board_type_no__board_type_no=3).count(),
        "activity_num": Board.objects.filter(board_type_no__board_type_no=4).count(),
        "contest_num": ContestBoard.objects.all().count(),
        "alpha_num": Board.objects.filter(board_type_no__board_type_no=6).count(),
        "beta_num": Board.objects.filter(board_type_no__board_type_no=7).count(),
    }


# ---- get_context_of_board_ ---- #
# INPUT : 게시글 번호
# OUTPUT : 없음
# RETURN : dict Type / 해당 게시글에 관련된 정보(파일, 댓글, 제목, 내용 등)를 context 변수로 반환
# 작성자 : 유동현
# 마지막 수정 일시 : 2021.04.13
def get_context_of_board_(board_no):
    board = Board.objects.get(pk=board_no)  # 해당 공모전 정보 db에서 불러오기

    # 게시글 파일 받아오기. (순서대로 전체파일, 이미지파일, 문서파일)
    board_file_list, image_list, doc_list = FileController.get_images_and_files_of_(board)  # 공모전 이미지와 문서 받아오기

    context = {
        "board": board,
        "file_list": doc_list,
        "img_list": image_list,
        'board_file_list': board_file_list,
        "board_type_no": board.board_type_no.board_type_no,
        "board_name": board.board_type_no.board_type_name,
        "board_exp": board.board_type_no.board_type_exp,
    }

    return context


def get_context_by_board_type(board_type: BoardType):
    return {
        "board_type_no": board_type.board_type_no,
        "board_name": board_type.board_type_name,
        "board_exp": board_type.board_type_exp
    }


# ---- get_context_of_contest_ ---- #
# INPUT : 공모전 게시글 번호
# OUTPUT : 없음
# RETURN : dict Type / 해당 게시글에 관련된 정보(파일, 댓글, 제목, 내용 등)를 context 변수로 반환
# 작성자 : 유동현
# 마지막 수정 일시 : 2021.04.13
def get_context_of_contest_(contest_no):
    contest = ContestBoard.objects.get(pk=contest_no)  # 해당 공모전 정보 db에서 불러오기
    # 게시글 파일 받아오기. (순서대로 전체파일, 이미지파일, 문서파일)
    contest_file_list, image_list, doc_list = FileController.get_images_and_files_of_(contest)  # 공모전 이미지와 문서 받아오기

    context = {
        'contest': contest,
        'file_list': doc_list,
        'image_list': image_list,
        'contest_file_list': contest_file_list,
        "board_name": "공모전 게시판",
        "board_exp": "공모전 정보를 알려주는 게시판",
    }

    return context


# ---- board_view ---- #
# : 게시글 목록 페이지
# 작성자 : 양태영
# 마지막 수정 일시 :
@login_required
def board_view(request, board_type_no):  # 게시판 페이지로 이동
    cur_user = get_logined_user(request)
    board_fixed_list = Board.objects.filter(
        Q(board_fixdate__gt=today()) & Q(board_type_no__board_type_no=board_type_no)).order_by("-board_fixdate")
    if board_type_no == 5:
        board_fixed_list = Board.objects.filter(
            Q(board_fixdate__gt=today()) & Q(board_type_no__board_type_no=1)).order_by("-board_fixdate")
        board_list = Board.objects.filter(board_type_no__board_type_no__lte=4).select_related("board_writer").order_by(
            "board_type_no").order_by("-board_created")
    elif board_type_no == 8:
        if role_check(cur_user, 4, "lte"):  # 회장단인 경우
            board_list = Board.objects.filter(board_type_no__board_type_no=board_type_no).select_related(
                "board_writer").order_by("-board_created")
        else:
            return not_allowed(request, msg="비정상적인 접근입니다.")
    elif board_type_no == 9:  # 건의 게시판의 경우(1대1로 진행해야 함)
        if role_check(cur_user, 4, "lte"):  # 회장단인 경우
            board_list = Board.objects.filter(board_type_no__board_type_no=board_type_no).select_related(
                "board_writer").order_by("-board_created")
        else:  # 회장단이 아닌 경우
            # 자신이 쓴 게시글만 확인
            board_list = Board.objects.filter(Q(board_type_no__board_type_no=board_type_no) & Q(
                board_writer=cur_user)).select_related("board_writer").order_by("-board_created")
    else:
        if 6 <= board_type_no <= 7 and cur_user.user_auth_id != 1:
            return not_allowed(request)
        board_list = Board.objects.filter(board_type_no__board_type_no=board_type_no).select_related(
            "board_writer").order_by("-board_created")

    board_list = get_page_object(request, board_list)
    context = {
        "board_fixed_list": board_fixed_list,
        "board_list": board_list,
        "board_name": BoardType.objects.get(pk=board_type_no).board_type_name,
        "board_exp": BoardType.objects.get(pk=board_type_no).board_type_exp,
        "board_type_no": board_type_no,
        "is_register_btn_show": is_register_btn_show(request, board_type_no)
    }
    context.update(get_sidebar_information())

    return render(request, 'board.html', context)


# ---- board_search ---- #
# : 게시글 검색
# 작성자 : 양태영
# 마지막 수정 일시 :
@auth_check()
def board_search(request, board_type_no):
    if request.method == "GET":
        cur_user = get_logined_user(request)
        keyword = request.GET.get("keyword")
        if 1 <= board_type_no <= 5:
            board_list = Board.objects.filter(
                Q(board_cont__icontains=keyword) |
                Q(board_title__icontains=keyword) |
                Q(board_writer__user_name__icontains=keyword)).filter(
                board_type_no__board_type_no__lte=3).select_related(
                "board_writer").order_by("-board_created").all()
        elif 6 <= board_type_no <= 7:
            if cur_user.user_auth_id != 1:
                return not_allowed(request)
            board_list = Board.objects.filter(
                Q(board_cont__icontains=keyword) |
                Q(board_title__icontains=keyword) |
                Q(board_writer__user_name__icontains=keyword)).filter(
                Q(board_type_no__board_type_no__gte=6) & Q(board_type_no__board_type_no__lte=7)).select_related(
                "board_writer").order_by("-board_created").all()
        elif 8 <= board_type_no <= 9:
            board_list = Board.objects.filter(
                Q(board_cont__icontains=keyword) |
                Q(board_title__icontains=keyword) |
                Q(board_writer__user_name__icontains=keyword)
            ).filter(board_type_no__board_type_no=board_type_no).select_related("board_writer").order_by(
                "-board_created")
            if board_type_no == 8 and not role_check(cur_user, role_no=4, sign="lte"):
                return not_allowed(request)
            if board_type_no == 9 and role_check(cur_user, 5, "gte"):
                board_list = board_list.filter(board_writer=get_logined_user(request))

        item = get_page_object(request, board_list)
        context = {
            "message": "\"" + keyword + "\"로 검색한 게시글이 존재하지 않습니다.",
            "board_list": item,
            'board_type_no': board_type_no,
            "board_name": "검색결과",
            "board_exp": "\"" + keyword + "\"로 검색한 결과입니다.",
        }
        context.update(get_sidebar_information())

        return render(request, "board.html", context)
    else:
        return redirect('board_view', board_type_no=5)


# ---- board_detail ---- #
# : 게시글 상세 페이지
# 작성자 : 양태영
# 마지막 수정 일시 : 2021.04.13 (유동현)
# 수정내용 : 코드 최적화
#   - context 변수 가져오는 함수 생성
@auth_check()
@exist_check
def board_detail(request, board_no):  # 게시글 상세 보기
    board = Board.objects.get(pk=board_no)
    if board.board_type_no.board_type_no == 4:
        return redirect("activity_detail", board_no=board_no)
    cur_user = get_logined_user(request)

    board_type_no = board.board_type_no.board_type_no
    if 6 <= board_type_no <= 7 and cur_user.user_auth_id != 1:
        return not_allowed(request)
    elif board_type_no == 8 and not role_check(cur_user, 4, "lte"):
        return not_allowed(request, "비 정상적인 접근입니다.")
    elif board_type_no == 9 and (board.board_writer != cur_user and not role_check(cur_user, 4, "lte")):
        return not_allowed(request, "비 정상적인 접근입니다.")
    context = get_context_of_board_(board_no)
    return render(request, 'board_detail.html', context)


# ---- board_register ---- #
# : 게시글 등록부
# 작성자 : 양태영
# 수정 일시 : #1. 2021.04.30 (유동현),
#            #2. 2021.07.22 (양태영)
# 수정내용 : #1. 모델 폼 적용에 따른 코드 수정
#           #2. 상단 고정 변수 추가
@auth_check()
def board_register(request):
    cur_user = get_logined_user(request)
    # 글쓰기 들어와서 등록 버튼을 누르면 실행이 되는 부분
    if request.method == "POST":
        board_form = BoardForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)
        # 게시글 상단 고정 여
        board_fixdate = get_fixdate(request)
        if board_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                board_param = {"board_writer": cur_user}
                if board_fixdate is not None:
                    board_param["board_fixdate"] = board_fixdate
                board = board_form.save(**board_param)
                file_form.save(instance=board)
                create_board_notice_alarm(board)
            return redirect("board_detail", board_no=board.board_no)
        else:
            return redirect(reverse("board_register"))

    else:  # 게시글 등록 버튼을 눌렀을 때
        board_type_no = BoardType.objects.get(pk=request.GET.get('board_type_no'))
        if board_type_no.board_type_no == 1 and not role_check(cur_user, 5,
                                                               "lte"):  # 공지사항 게시판에서 글쓰기 버튼을 눌렀을 경우 회장단이 아니면
            return not_allowed(request, "비 정상적인 접근입니다.")
        if 6 <= board_type_no.board_type_no <= 7 and cur_user.user_auth_id != 1:
            return not_allowed(request)
        if board_type_no.board_type_no == 8 and not role_check(cur_user, 4, "lte"):  # 회장단 게시판에서 글쓰기 버튼을 눌렀을 경우 회장단이 아니면
            return not_allowed(request, "비 정상적인 접근입니다.")
        context = {
            "board_form": BoardForm(initial={'board_type_no': board_type_no.board_type_no}),
            "file_form": FileForm(),
        }
        context.update(get_context_by_board_type(board_type_no))
        return render(request, "board_register.html", context)


# ---- board_update ---- #
# : 게시글 수정
# 작성자 : 양태영
# 마지막 수정 일시 : 2021.04.30 (유동현)
# 수정내용 : 모델 폼 적용에 따른 코드 수정
@writer_only()
def board_update(request, board_no):
    board = get_object_or_404(Board, pk=board_no)
    # 수정을 누르면 GET 방식으로 DB 에 있는 것을 꺼내 온다.
    if request.method == "GET":
        context = {
            'board_no': board_no,
            'board_type_no': board.board_type_no.board_type_no,
            'board_form': BoardForm(instance=board),
            'file_form': FileForm(),
            'file_list': BoardFile.objects.filter(file_fk=board)
        }
        context.update(get_context_by_board_type(board.board_type_no))
        return render(request, "board_register.html", context)

    # 수정을 하고 난 후 수정 버튼을 누를 경우 이걸로 진행 됌
    elif request.method == 'POST':
        board_form = BoardForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if board_form.is_valid():
            board_form.update(instance=board)
            board_fixdate = get_fixdate(request)
            if board_fixdate is not None:
                board.board_fixdate = get_fixdate(request)
                board.save()
            if file_form.is_valid():
                board_files = BoardFile.objects.filter(file_fk=board)  # 파일들을 갖고 옴
                FileController.remove_files_by_user(request, board_files)  # 사용자가 제거한 파일 삭제
                file_form.save(instance=board)  # 파일 업로드

        # 목록 페이지 이동
        return redirect("board_detail", board_no=board_no)


# ---- board_delete ---- #
# : 게시글 상세페이지에서 삭제하는 코드
# 작성자 : 양태영
# 마지막 수정 일시 : 2021.04.30 (유동현)
# 수정내용 : 모델폼 사용 => urls.py 변경에 따른 코드 수정
@writer_only(superuser=True)
def board_delete(request, board_no):
    cur_user = get_logined_user(request)
    board = Board.objects.get(pk=board_no)
    board_type_no = board.board_type_no.board_type_no
    with transaction.atomic():
        if board.board_writer != cur_user and role_check(cur_user, role_no=3, sign="lte"):
            delete_board_by_superuser_alarm(request, board)
        FileController.delete_all_files_of_(board)  # 해당 게시글에 등록된 파일 모두 제거
        comment_delete_by_post_delete(board)
        board.delete()  # 파일과 폴더 삭제 후, 게시글 DB 에서 삭제

    return redirect('board_view', board_type_no=board_type_no)


@auth_check(active=True)
def contest_view(request):
    # 공모전 게시물 전부를 해당 파일과 함께 Queryset 으로 가져오기
    contest_board_list = list(ContestBoard.objects.filter(contest_deadline__gte=today()).order_by(
        'contest_deadline').prefetch_related("files"))
    contest_board_list_expired = list(ContestBoard.objects.filter(contest_deadline__lt=today()).order_by(
        "contest_deadline").prefetch_related("files"))
    contest_board_list.extend(contest_board_list_expired)
    # pagination 을 위한 page 객체 (page 객체 안에는 한 페이지에 보여줄만큼의 게시물이 들어있다.)
    contest_list = get_page_object(request, contest_board_list, num_of_boards_in_one_page=4)

    context = {
        "contest_list": contest_list,
        "board_name": "공모전 게시판",
        "board_exp": "공모전 정보를 알려주는 게시판"
    }
    # update() 는 dict 자료형을 이어주는 함수. list.append() 와 같은 함수
    context.update(get_sidebar_information())

    return render(request, 'contest_board.html', context)


# ---- contest_register ---- #
# : 공모전 글 등록하기
# 작성자 : 유동현
# 마지막 수정 일시 : 2021.04.30
# 수정내용 : 모델 폼으로 처리하는 걸로 코드 수정
# 버그 처리해야할 사항 :: 등록 버튼 누르고 가끔 로딩되면서 화면전환이 늦어질 때가 있는데,
#                      그 때 등록버튼 연타하면 클릭한수만큼 동일한 게시글 작성됨.
@superuser_only()
def contest_register(request):  # 공모전 등록
    if request.method == 'POST':
        contest_form = ContestForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)
        if contest_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                # 학번 오류 처리 필요
                # 파일 저장시 오류 발생하거나, 로딩 중 저장 여러번 누르는 등 부적절한 저장 피하기 => 트랜젝션
                contest = contest_form.save(
                    contest_writer=get_logined_user(request))
                file_form.save(instance=contest)
                messages.success(request, '게시글을 성공적으로 등록하셨습니다.')
                return redirect("contest_detail", contest_no=contest.contest_no)

    # 목록에서 신규 등록 버튼 눌렀을때
    elif request.method == 'GET':
        form_context = {
            'contest_form': ContestForm(),
            'file_form': FileForm(),
        }
        return render(request, 'contest_register.html', form_context)


# ---- contest_detail ---- #
# : 공모전 글 상세페이지
# 작성자 : 유동현
# 마지막 수정 일시 : 2021.04.13
# 수정내용 :
@exist_check
@auth_check(active=True)
def contest_detail(request, contest_no):  # 게시판 상세 페이지로 이동
    if request.method == 'GET':
        try:
            context = get_context_of_contest_(contest_no)
            return render(request, 'contest_detail.html', context)
        except ContestBoard.DoesNotExist:
            messages.warning(request, "해당 공모전을 찾을 수 없습니다. 삭제되었을 수 있습니다.")
            return redirect(reverse("contest_list"))
    else:  # 비정상적인 접근
        return redirect(reverse('contest_list'))


# ---- contest_delete ---- #
# : 공모전 글 삭제
# 작성자 : 유동현
# 마지막 수정 일시 : 2021.04.30
# 수정내용 : 모델 폼 사용 => urls.py 변경에 따른 코드 수정
@writer_only(superuser=True)
def contest_delete(request, contest_no):
    contest = ContestBoard.objects.get(pk=contest_no)

    with transaction.atomic():
        FileController.delete_all_files_of_(contest)  # 해당 게시글에 등록된 파일 모두 제거
        comment_delete_by_post_delete(contest)
        contest.delete()  # 파일과 폴더 삭제 후, 게시글 DB 에서 삭제

    return redirect(reverse('contest_list'))


# ---- contest_update ---- #
# : 공모전 글 수정
# 작성자 : 유동현
# 마지막 수정 일시 : 2021.04.30
# 수정내용 : 모델 폼 사용 => urls.py 변경에 따른 코드 수정
# 버그 처리해야할 사항 :: 수정 버튼 누르고 가끔 로딩되면서 화면전환이 늦어질 때가 있는데,
#                      그 때 수정버튼 연타하면 클릭한수만큼 동일한 게시글 작성됨.
@writer_only()
def contest_update(request, contest_no):
    contest = get_object_or_404(ContestBoard, pk=contest_no)
    # 게시물 상세보기에서 수정하기 버튼 눌렀을 때
    if request.method == "GET":
        context = {
            'contest_no': contest_no,
            'contest_form': ContestForm(instance=contest),
            'file_form': FileForm(),
            'file_list': ContestFile.objects.filter(file_fk=contest)
        }
        return render(request, 'contest_register.html', context)

    # 게시물 수정을 완료했을 때
    elif request.method == "POST":
        contest_form = ContestForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if contest_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                contest_form.update(instance=contest)
                contest_files = ContestFile.objects.filter(file_fk=contest)  # 게시글 파일을 불러옴
                FileController.update_file_by_file_form(request=request, instance=contest, file_form=file_form,
                                                        files=contest_files, required=True)
            # 수정된 게시글 페이지로 이동
            return redirect("contest_detail", contest_no=contest.contest_no)
        else:
            return redirect(request.path)


# 공모전 검색
@auth_check(active=True)
def contest_search(request):
    if request.method == "GET":
        # 키워드를 GET 파라미터로 받음
        keyword = request.GET.get("keyword")
        # 제목, 내용, 글쓴이 이름, 주최기관, 주제에 관련해 키워드가 포함되는지 검색
        contest_list = ContestBoard.objects.filter(
            Q(contest_title__icontains=keyword) |
            Q(contest_cont__icontains=keyword) |
            Q(contest_writer__user_name__icontains=keyword) |
            Q(contest_asso__icontains=keyword) |
            Q(contest_topic__icontains=keyword)
        )
        # 페이지 가능하게 해당 공모전 리스트를 변화시킴.
        contest_list = get_page_object(request, model_list=contest_list, num_of_boards_in_one_page=4)
        # 컨텍스트 등록.
        context = {
            "contest_list": contest_list,
            "board_name": "공모전 검색 결과",
            "board_exp": '"' + keyword + '"로 검색한 결과입니다.'
        }
        # 컨텍스트 사이드바 옵션 가져옴.
        context.update(get_sidebar_information())
        return render(request, 'contest_board.html', context)
    else:
        return redirect(reverse("contest_list"))
