from django.db import transaction
from django.shortcuts import render, get_object_or_404, reverse, redirect
from DB.models import Alarm, Board, BoardFile, History, User
from board.forms import FileForm
from main.forms import ActivityForm
from pagination_handler import *
from file_controller import FileController
from django.db.models import Q
from django.http import HttpResponseRedirect
from user_controller import login_required, writer_only, auth_check, superuser_only, get_logined_user
from exception_handler import exist_check
from DB.models import UserSchedule
from date_controller import is_user_recruiting, is_interview_progress
from post_controller import comment_delete_by_post_delete
from django.contrib import messages


# 메인페이지 이동 함수
def index(request):
    from member import session
    # 임시 로그인
    # session.save_session(request, user_model=User.objects.get(pk=12162359), logined_email="0130yang@gmail.com", provider="google")
    # session.save_session(request, user_model=User.objects.get(pk=12171652))
    # session.save_session(request, user_model=User.objects.get(pk=12172285))
    # session.save_session(request, user_model=User.objects.get(pk=12172434))
    context = {
        "is_user_recruiting": is_user_recruiting(),
        "is_interview_progress": is_interview_progress(),
        "user_schedule": UserSchedule.objects.get(pk=1)
    }
    return render(request, "index.html", context)


# 동아리 소개를 출력하기 위한 뷰 함수.
def introduce(request):
    # 히스토리 내역을 가져옴
    history_list = History.objects.all().order_by("history_date")
    # 연도당 하나만 띄우기 위해서 히스토리에 등록된 것들의 연도만 뽑아옴. 연도 리스트.
    year_list = list(range(history_list.first().history_date.year, history_list.last().history_date.year + 1))
    # 연도가 띄워질 연혁을 담기 위한 리스트
    mark_list = []
    # year당 제일 처음 있는 것을 mark함.
    for year in year_list:
        mark_list.append(History.objects.filter(history_date__year=year).order_by("history_date").first().history_no)
    chief_crews = User.objects.filter(Q(user_role__role_no__lte=4) & Q(user_auth__auth_no=1)).order_by("user_role__role_no").all()
    for history in history_list:
        for mark in mark_list:
            if history.history_no == mark:
                history.is_marked = True
                break
            else:
                history.is_marked = False
    context = {
        "history_list": history_list
    }
    if len(chief_crews) != 0:
        # 회장단인 사람의 객체를 가져오고 등록, chief_carrier에서 이력 정보도 함께 가져옴
        context['chief_crews'] = chief_crews
    return render(request, 'introduce.html', context)  # introduce 에 실어서 보내분다.


# 동아리 활동 게시판
# ---- activity ---- #
# : 게시글 목록 페이지
# 작성자 : 양태영
# 마지막 수정 일시 : 2021.04.15 (유동현)
# 수정 내역:
#   - 코드 최적화 paginator 부분
def activity_list(request):
    # 최신순으로 정렬하고, 1:M 관계로 가져오기 위해 prefetch_related 함수 사용
    board_list = Board.objects.filter(board_type_no__board_type_no=4).order_by('-board_created').prefetch_related(
        "files")
    board_list = get_page_object(request, board_list, 6)

    return render(request, 'activity_list.html', {'board_list': board_list})


# 동아리 활동 게시판 상세보기
# ---- activity_detail ---- #
# : 게시글 상세 페이지
# 작성자 : 양태영
# 마지막 수정 일시 : 2021.04.15 (유동현)
# 수정 내역:
#   - 단순 코드 정리..
@exist_check
def activity_detail(request, board_no):
    if board_no is not None:
        board = Board.objects.get(pk=board_no)
        if board.board_type_no.board_type_no != 4:
            messages.warning(request, "해당 게시글이 존재하지 않습니다. 삭제되었을 수 있습니다.")
            return redirect("activity")
        context = {
            "board": board,
            "board_file_list": BoardFile.objects.filter(file_fk=board),
        }
        return render(request, 'activity_detail.html', context)
    else:
        return redirect(reverse('activity'))


# 동아리 활동 게시판 등록하기
# ---- activity_register ---- #
# 작성자 : 양태영
# 마지막 수정 일시 : 2021.05.04 (유동현)
# 수정내용 : 폼 처리
@superuser_only()
def activity_register(request):
    # 글쓰기 들어와서 등록 버튼을 누르면 실행이 되는 부분
    if request.method == "POST":
        activity_form = ActivityForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if activity_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                activity = activity_form.save(
                    board_writer=User.objects.get(pk=request.session.get('user_stu')))
                file_form.save(instance=activity)

            return redirect("activity_detail", board_no=activity.board_no)
        else:
            return redirect(reverse("activity"))

    else:  # 게시글 등록 버튼을 눌렀을 때
        context = {
            "board_form": ActivityForm(),
            "file_form": FileForm(),
        }
        return render(request, "activity_register.html", context)


# : 동아리 글 수정 코드
# ---- activity_update ---- #
# 작성자 : 양태영
# 마지막 수정 일시 : 2021.05.04 (유동현)
# 수정내용 : 폼 처리
@writer_only(superuser=False)
def activity_update(request, board_no):
    board = get_object_or_404(Board, pk=board_no)

    # 수정을 누르면 GET 방식으로 DB 에 있는 것을 꺼내 온다.
    if request.method == "GET":
        context = {
            'board_no': board_no,
            'board_form': ActivityForm(instance=board),
            'file_form': FileForm(),
            'file_list': BoardFile.objects.filter(file_fk=board)
        }

        return render(request, 'activity_register.html', context)  # 이거로 보내줘서 작업 가능

    # 수정을 하고 난 후 수정 버튼을 누를 경우 이걸로 진행 됌
    elif request.method == 'POST':
        activity_form = ActivityForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if activity_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                activity_form.update(instance=board)
                board_files = BoardFile.objects.filter(file_fk=board)  # 파일들을 갖고 옴
                FileController.remove_files_by_user(request, board_files)  # 사용자가 제거한 파일 삭제
                file_form.save(instance=board)  # 파일 업로드

        # 목록 페이지 이동
        return redirect("activity_detail", board_no=board.board_no)

    # 잘못 왔을 경우
    return redirect("activity")


# : 활동게시판 상세페이지에서 삭제하는 코드
# ---- activity_delete ---- #
# 작성자 : 양태영
# 마지막 수정 일시 : 2021.05.04 (유동현)
# 수정내용 : 트랜젝션 코드 추가
@writer_only(superuser=True)
def activity_delete(request, board_no):
    board = Board.objects.get(pk=board_no)
    comment_delete_by_post_delete(board)
    with transaction.atomic():
        FileController.delete_all_files_of_(board)  # 해당 게시글에 등록된 파일 모두 제거
        comment_delete_by_post_delete(board)
        board.delete()  # 파일과 폴더 삭제 후, 게시글 DB 에서 삭제

    return redirect(reverse('activity'))


# ---- history_register ---- #
# : 연혁 등록하는 코드
# 작성자 : 양태영
# 마지막 수정 일시 : 2021.04.15 (유동현)
# 수정내용
#   - 단순 코드 정리 history.save 없애도 되서 없앴음.
@superuser_only(cfo_included=False)
def history_register(request):  # 연혁 등록
    history_title = request.POST.get("history_title")
    history_cont = request.POST.get("history_cont")
    if history_cont == "":
        history_cont = history_title
    if request.method == "POST":  # 정상적으로 값이 넘어왔을 경우
        History.objects.create(  # history 객체 생성 후 받은 값을 집어넣음.
            history_title=history_title,
            history_cont=history_cont,
            history_date=request.POST.get("history_date"),
            history_writer=get_logined_user(request)
        )
        return redirect(reverse("introduce"))  # 소개 페이지로 리다이렉트

    else:  # 비 정상적인 경로로 접근하였을 경우 (해킹 시도)
        print("비정상적인 접근: ", request.session.get("user_stu"))
        return render(request, "index.html", {'lgn_is_failed': 1})


# ---- history_update ---- #
# : 연혁 수정하는 코드
# 작성자 : 양태영
# 마지막 수정 일시 :
@superuser_only(cfo_included=False)
def history_update(request):  # 연혁 수정
    if request.method == "POST":  # 정상적으로 파라미터가 넘어왔을 경우
        history = History.objects.get(pk=request.POST.get("history_no"))  # 가져온 history_no를 토대로 수정 내역을 적용
        if history_title := request.POST.get("history_title"):
            history.history_title = history_title
        if history_cont := request.POST.get("history_cont"):
            history.history_cont = history_cont
        if history_date := request.POST.get("history_date"):
            history.history_date = history_date
        history.history_writer = get_logined_user(request)
        history.save()
        return redirect(reverse("introduce"))
    else:  # 비정상적인 접근의 경우 (해킹시도)
        return redirect("index")  # 메인페이지로 보내버림


# ---- history_delete ---- #
# : 연혁 삭제하는 코드
# 작성자 : 양태영
# 마지막 수정 일시 :
@superuser_only(cfo_included=False)
def history_delete(request):  # 연혁 삭제
    if request.method == "POST":  # 정상적으로 파라미터가 넘어왔을 경우
        history = History.objects.get(pk=request.POST.get("history_no"))  # 가져온 history_no를 토대로 삭제할 대상을 가져옴
        history.delete()  # 삭제
        return redirect(reverse("introduce"))  # 소개 페이지로 리다이렉팅
    else:  # 비정상적인 접근의 경우(해킹시도)
        return redirect(reverse("index"))  # 메인페이지로 보내버림


@login_required
def alarm_check(request, alarm_no):
    alarm = Alarm.objects.get(pk=alarm_no)
    alarm.alarm_ischecked = 1
    alarm.save()
    return HttpResponseRedirect(alarm.alarm_link)


# 명예의 전당
@auth_check()
def hall_of_fame(request):
    context = {
        "graduated_user_list": User.objects.filter(Q(user_apply_publish=1) & Q(user_grade=0))
    }
    return render(request, "hall_of_fame.html", context)
