from django.db import transaction
from django.shortcuts import render, redirect, reverse, get_object_or_404
from DB.models import Board, BoardType, Comment, ContestBoard, ContestComment, User
from django.db.models import Q
from board.forms import *
from pagination_handler import get_page_object
from alarm.alarm_controller import create_comment_alarm, create_comment_ref_alarm
from user_controller import login_required, writer_only


# ---- get_sidebar_information ---- #
# INPUT : Board 객체 or ContestBoard 객체
# OUTPUT : 없음
# RETURN : dict Type / 각 게시판의 게시글 수
# 작성자 : 유동현
# 마지막 수정 일시 : 2021.04.13
def get_sidebar_information():
    return {
        "all_num": Board.objects.all().count(),
        "notice_num": Board.objects.filter(board_type_no__board_type_no=1).count(),
        "free_num": Board.objects.filter(board_type_no__board_type_no=2).count(),
        "quest_num": Board.objects.filter(board_type_no__board_type_no=3).count(),
        "activity_num": Board.objects.filter(board_type_no__board_type_no=4).count(),
        "contest_num": ContestBoard.objects.all().count(),
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
    board_file_list, image_list, doc_list = get_images_and_files_of_(board)  # 공모전 이미지와 문서 받아오기

    # 댓글 불러오기
    comment_list = Comment.objects.filter(comment_board_no=board).filter(comment_cont_ref__isnull=True).order_by(
        "comment_created").prefetch_related("comment_set")

    context = {
        "board": board,
        "file_list": doc_list,
        "img_list": image_list,
        'board_file_list': board_file_list,
        "comment_list": comment_list,
        "board_type_no": board.board_type_no.board_type_no,
        "board_name": board.board_type_no.board_type_name,
        "board_exp": board.board_type_no.board_type_exp,
    }

    return context


# ---- get_context_of_contest_ ---- #
# INPUT : 공모전 게시글 번호
# OUTPUT : 없음
# RETURN : dict Type / 해당 게시글에 관련된 정보(파일, 댓글, 제목, 내용 등)를 context 변수로 반환
# 작성자 : 유동현
# 마지막 수정 일시 : 2021.04.13
def get_context_of_contest_(contest_no):
    contest = ContestBoard.objects.get(pk=contest_no)  # 해당 공모전 정보 db에서 불러오기
    # 게시글 파일 받아오기. (순서대로 전체파일, 이미지파일, 문서파일)
    contest_file_list, image_list, doc_list = get_images_and_files_of_(contest)  # 공모전 이미지와 문서 받아오기

    # 댓글 불러오기
    comment_list = ContestComment.objects.filter(comment_board_no=contest).filter(
        comment_cont_ref__isnull=True).order_by("comment_created").prefetch_related("contestcomment_set")

    context = {
        'contest': contest,
        'file_list': doc_list,
        'image_list': image_list,
        'contest_file_list': contest_file_list,
        "board_name": "공모전 게시판",
        "board_exp": "공모전 정보를 알려주는 게시판",
        "comment_list": comment_list,
    }

    return context


# ---- board_view ---- #
# : 게시글 목록 페이지
# 작성자 : 양태영
# 마지막 수정 일시 :
def board_view(request, board_type_no):  # 게시판 페이지로 이동
    if board_type_no == 5:
        board_list = Board.objects.all().select_related("board_writer").order_by(
            "board_type_no").order_by("-board_created")
    else:
        board_list = Board.objects.filter(board_type_no=BoardType.objects.get(pk=board_type_no)).select_related(
            "board_writer").order_by("-board_created")

    item = get_page_object(request, board_list)
    context = {
        "board_list": item,
        "board_name": BoardType.objects.get(pk=board_type_no).board_type_name,
        "board_exp": BoardType.objects.get(pk=board_type_no).board_type_exp,
        "board_type_no": board_type_no,
    }
    context.update(get_sidebar_information())

    return render(request, 'board.html', context)


# ---- board_search ---- #
# : 게시글 검색
# 작성자 : 양태영
# 마지막 수정 일시 :
def board_search(request):
    if request.method == "GET":
        keyword = request.GET.get("keyword")
        board_list = Board.objects.filter(
            Q(board_cont__icontains=keyword) | Q(board_title__icontains=keyword) | Q(
                board_writer__user_name__icontains=keyword)).select_related("board_writer").order_by(
            "-board_created").all()

        item = get_page_object(request, board_list)
        context = {
            "message": "\"" + keyword + "\"로 검색한 게시글이 존재하지 않습니다.",
            "board_list": item,
            'board_type_no': 5,
            "board_name": "검색결과",
            "board_exp": keyword + "로 검색한 결과입니다.",
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
def board_detail(request, board_no):  # 게시글 상세 보기
    context = get_context_of_board_(board_no)

    return render(request, 'board_detail.html', context)


# ---- board_register ---- #
# : 게시글 등록
# 작성자 : 양태영
# 마지막 수정 일시 : 2021.04.30 (유동현)
# 수정내용 : 모델 폼 적용에 따른 코드 수정
@login_required
def board_register(request):
    # 글쓰기 들어와서 등록 버튼을 누르면 실행이 되는 부분
    if request.method == "POST":
        board_form = BoardForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if board_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                board = board_form.save(
                    board_writer=User.objects.get(pk=request.session.get('user_stu')))
                file_form.save(instance=board)

            return redirect("board_detail", board_no=board.board_no)
        else:
            return redirect("board_view", board_type_no=5)

    else:  # 게시글 등록 버튼을 눌렀을 때
        board_type_no = BoardType.objects.get(pk=request.GET.get('board_type_no'))
        context = {
            "board_type_no": board_type_no.board_type_no,
            "board_name": board_type_no.board_type_name,
            "board_exp": board_type_no.board_type_exp,
            "board_form": BoardForm(board_type_no=board_type_no.board_type_no),
            "file_form": FileForm(),
        }
        return render(request, "board_register.html", context)


# ---- board_update ---- #
# : 게시글 수정
# 작성자 : 양태영
# 마지막 수정 일시 : 2021.04.30 (유동현)
# 수정내용 : 모델 폼 적용에 따른 코드 수정
@login_required
@writer_only
def board_update(request, board_no):
    board = get_object_or_404(Board, pk=board_no)

    # 수정을 누르면 GET 방식으로 DB 에 있는 것을 꺼내 온다.
    if request.method == "GET":
        context = {
            'board_no': board_no,
            'board_type_no': board.board_type_no.board_type_no,
            'board_form': BoardForm(instance=board),
            'file_form': FileForm(),
            'file_list': BoardFile.objects.filter(board_no=board)
        }
        return render(request, "board_register.html", context)

    # 수정을 하고 난 후 수정 버튼을 누를 경우 이걸로 진행 됌
    elif request.method == 'POST':
        board_form = BoardForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if board_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                board_form.update(pk=board_no)
                board_files = BoardFile.objects.filter(board_no=board)  # 파일들을 갖고 옴
                remove_files_by_user(request, board_files)  # 사용자가 제거한 파일 삭제
                file_form.save(instance=board)

        # 목록 페이지 이동
        return redirect("board_detail", board_no=board_no)


# ---- board_delete ---- #
# : 게시글 상세페이지에서 삭제하는 코드
# 작성자 : 양태영
# 마지막 수정 일시 : 2021.04.30 (유동현)
# 수정내용 : 모델폼 사용 => urls.py 변경에 따른 코드 수정
@login_required
@writer_only
def board_delete(request, board_no):
    board = Board.objects.get(pk=board_no)

    with transaction.atomic():
        delete_all_files_of_(board)  # 해당 게시글에 등록된 파일 모두 제거
        board.delete()  # 파일과 폴더 삭제 후, 게시글 DB 에서 삭제

    return redirect('board_view', board_type_no=5)


# 댓글 달기 코드
@login_required
def board_comment_register(request):
    if request.method == "POST":
        board = Board.objects.get(pk=request.POST.get('board_no'))  # 게시글 번호 들고오는 것임

        comment = Comment.objects.create(
            comment_board_no=board,  # 해당 게시글에
            comment_writer=User.objects.get(pk=request.session.get('user_stu')),  # 해당 학번이
            comment_cont=request.POST.get('comment_cont')  # 사용자가 쓴 내용을 가져옴
        )
        create_comment_alarm(comment)

    else:
        board = Board.objects.get(pk=request.GET.get('board_no'))  # 게시글 번호 들고오는 것임
        # 객체로 받아서 저장할 예정
        comment = Comment.objects.create(
            comment_board_no=board,
            comment_writer=User.objects.get(pk=request.session.get('user_stu')),
            comment_cont=request.GET.get('comment_cont'),
            comment_cont_ref=Comment.objects.get(pk=request.GET.get("comment_ref"))
        )
        create_comment_ref_alarm(comment)

        # 데이터 베이스에 저장
    return redirect("board_detail", board_no=board.board_no)


# 댓글 삭제 코드
@login_required
def board_comment_delete(request):
    if request.method == "POST":  # 댓글 삭제를 누를 경우
        board_no = request.POST.get('board_no')
        comment = Comment.objects.get(pk=request.POST.get('comment_id'))
        comment.delete()
        return redirect("board_detail", board_no=board_no)  # 게시글 상세페이지로 이동
    else:
        return redirect("board_view", board_type_no=5)  # 잘못 들어온 접근은 전체 게시판으로 이동


# 댓글 수정 코드
@login_required
def board_comment_update(request):
    if request.method == "POST":  # 정상적으로 파라미터가 넘어왔을 경우
        board_no = request.POST.get('board_no')
        comment = Comment.objects.get(pk=request.POST.get('comment_id'))  # 가져온 comment_id를 토대로 수정 내역을 적용
        comment.comment_cont = request.POST.get('comment_cont')  # 수정할 내용을 가져옴
        comment.save()  # DB 저장
        return redirect("board_detail", board_no=board_no)  # 게시글 상세 페이지로 돌아감
    else:
        return redirect("board_view", board_type_no=5)  # 잘못된 요청의 경우 전체 게시판으로 이동하게 함.


# ---- contest_list ---- #
# : 공모전 글 목록 페이지
# 작성자 : 유동현
# 마지막 수정 일시 : 2021.04.13
# 수정내용 :
def contest_list(request):
    # 공모전 게시물 전부를 해당 파일과 함께 Queryset 으로 가져오기
    contest_board_list = ContestBoard.objects.all().order_by('-contest_deadline').prefetch_related("contestfile_set")

    # pagination 을 위한 page 객체 (page 객체 안에는 한 페이지에 보여줄만큼의 게시물이 들어있다.)
    item = get_page_object(request, contest_board_list, num_of_boards_in_one_page=6)

    context = {
        "contest_list": item,
        "board_name": "공모전 게시판",
        "board_exp": "공모전 정보를 알려주는 게시판",
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
@login_required
def contest_register(request):  # 공모전 등록
    if request.method == 'POST':
        contest_form = ContestForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if contest_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                # 학번 오류 처리 필요
                # 파일 저장시 오류 발생하거나, 로딩 중 저장 여러번 누르는 등 부적절한 저장 피하기 => 트랜젝션
                contest = contest_form.save(
                    contest_writer=User.objects.get(pk=request.session.get('user_stu')))
                file_form.save(instance=contest)
        else:
            pass

        # form의 유효성과 관계없이 게시글 목록으로 이동
        return redirect(reverse('contest_list'))

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
def contest_detail(request, contest_no):  # 게시판 상세 페이지로 이동
    if request.method == 'GET':
        context = get_context_of_contest_(contest_no)
        return render(request, 'contest_detail.html', context)

    else:  # 비정상적인 접근
        print(request)  # LOGGING :: 로그 파일 생성하는 코드 나중에 수정해야 함.
        return redirect(reverse('contest_list'))


# ---- contest_delete ---- #
# : 공모전 글 삭제
# 작성자 : 유동현
# 마지막 수정 일시 : 2021.04.30
# 수정내용 : 모델 폼 사용 => urls.py 변경에 따른 코드 수정
@login_required
@writer_only
def contest_delete(request, contest_no):
    contest = ContestBoard.objects.get(pk=contest_no)

    with transaction.atomic():
        delete_all_files_of_(contest)  # 해당 게시글에 등록된 파일 모두 제거
        contest.delete()  # 파일과 폴더 삭제 후, 게시글 DB 에서 삭제

    return redirect(reverse('contest_list'))


# ---- contest_update ---- #
# : 공모전 글 수정
# 작성자 : 유동현
# 마지막 수정 일시 : 2021.04.30
# 수정내용 : 모델 폼 사용 => urls.py 변경에 따른 코드 수정
# 버그 처리해야할 사항 :: 수정 버튼 누르고 가끔 로딩되면서 화면전환이 늦어질 때가 있는데,
#                      그 때 수정버튼 연타하면 클릭한수만큼 동일한 게시글 작성됨.
@login_required
@writer_only
def contest_update(request, contest_no):
    contest = get_object_or_404(ContestBoard, pk=contest_no)

    # 게시물 상세보기에서 수정하기 버튼 눌렀을 때
    if request.method == "GET":
        context = {
            'contest_no': contest_no,
            'contest_form': ContestForm(instance=contest),
            'file_form': FileForm(),
            'file_list': ContestFile.objects.filter(contest_no=contest)
        }
        return render(request, 'contest_register.html', context)

    # 게시물 수정을 완료했을 때
    elif request.method == "POST":
        contest_form = ContestForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if contest_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                contest_form.update(pk=contest_no)
                contest_files = ContestFile.objects.filter(contest_no=contest)  # 게시글 파일을 불러옴
                remove_files_by_user(request, contest_files)  # 사용자가 삭제한 파일을 제거
                file_form.save(contest)  # 유효성 검사 문제. 썸네일이 보장되는가..?

            # 수정된 게시글 페이지로 이동
            return redirect("contest_detail", contest_no=contest.contest_no)
        else:
            return redirect(reverse('contest_list'))


# ---- contest_comment_update ---- #
# : 공모전 댓글 수정
# 작성자 : 유동현
# 마지막 수정 일시 : 2021.04.15
# 수정내용 :
@login_required
def contest_comment_update(request):
    if request.method == "POST":
        contest_no = request.POST.get("contest_no")
        comment = ContestComment.objects.get(pk=request.POST.get("comment_id"))
        comment.comment_cont = request.POST.get("comment_cont")
        comment.save()

        return redirect("contest_detail", contest_no=contest_no)


# ---- contest_comment_delete ---- #
# : 공모전 댓글 삭제
# 작성자 : 유동현
# 마지막 수정 일시 : 2021.04.15
# 수정내용 :
@login_required
def contest_comment_delete(request):
    if request.method == "POST":
        contest_no = request.POST.get('contest_no')
        comment = ContestComment.objects.get(pk=request.POST.get('comment_id'))
        comment.delete()
        return redirect("contest_detail", contest_no=contest_no)
    else:
        return render(request, "contest_board.html")


# ---- contest_comment_register ---- #
# : 공모전 댓글 등록
# 작성자 : 유동현
# 마지막 수정 일시 : 2021.04.15
# 수정내용 :
@login_required
def contest_comment_register(request):
    contest = None

    # 댓글 등록할 때
    if request.method == "POST":
        contest = ContestBoard.objects.get(pk=request.POST.get("contest_no"))
        ContestComment.objects.create(
            comment_writer=User.objects.get(user_stu=request.session.get("user_stu")),
            comment_cont=request.POST.get("comment_cont"),
            comment_board_no=contest
        )

    # 대댓글 등록할 때
    elif request.method == "GET":
        contest = ContestBoard.objects.get(pk=request.GET.get("board_no"))  # sy.js AddReply 함수. <input name='board_no'>
        ContestComment.objects.create(
            comment_writer=User.objects.get(user_stu=request.session.get("user_stu")),
            comment_cont=request.GET.get("comment_cont"),
            comment_board_no=contest,
            comment_cont_ref=ContestComment.objects.get(pk=request.GET.get("comment_ref"))
        )

    return redirect("contest_detail", contest_no=contest.contest_no)

