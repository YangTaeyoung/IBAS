from django.shortcuts import render, get_object_or_404, reverse, redirect
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from DB.models import AuthUser, User, ChiefCarrier, UserRole, Board, BoardFile, \
    BoardType, Comment, History  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from django.db.models import Q
from member import session
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.conf import settings
from IBAS.user_controller import is_chief_exist, get_chief
import os


# 메인페이지 이동 함수
def index(request):
    # 임시 로그인
    session.save_session(request, User.objects.get(pk=12162359))

    if is_chief_exist():
        chief = get_chief()  # 하단바에서 회장꺼만 들고오면 됌
        session.save_chief(request, chief)  # 회장꺼 세션에 저장시켜줬음. save_chief 함수는 session 에 있음.
    context = {}
    return render(request, "index.html", context)


# 동아리 소개 작업할 것임
def introduce(request):
    # 히스토리 내역을 가져옴
    context = {'history_list': History.objects.all().order_by("history_date")}

    if len(User.objects.filter(~Q(user_role=UserRole.objects.get(pk=5))).prefetch_related(
            'chiefcarrier_set').all()) != 0:
        # 회장단인 사람의 객체를 가져오고 등록, Chief_carrier에서 이력 정보도 함께 가져옴
        context['chief_crews'] = User.objects.filter(~Q(user_role=UserRole.objects.get(pk=5))).prefetch_related(
            'chiefcarrier_set').all()
    return render(request, 'introduce.html', context)  # introduce 에 실어서 보내분다.


# 동아리 활동 게시판
def activity(request):
    # 최신순으로 정렬하고, 1:M 관계로 가져오기 위해 prefetch_related 함수 사용
    board_list = Board.objects.filter(board_type_no__board_type_no=4).order_by('-board_created').prefetch_related(
        "boardfile_set")
    # board 에서 board_type_no = 5 인 것만 들고옴. 최신 순으로 보여주는 코드는 order_by
    # board_type_no = 5 <- 동아리게시판에 관련한 글만 가져오기 위해서 만들어짐
    paginator = Paginator(board_list, 6)  # 페이지네이터로 10개씩 보이게끔. 나중에 수정하면 됌
    page = request.GET.get('page')  # 페이지 이름 ㅇㅇ 여기서 변경하면 됌
    item = paginator.get_page(page)
    context = {
        'board_list': item,
        "board_len": len(board_list)
    }
    return render(request, 'activity_list.html', context)


# 동아리 활동 게시판 상세보기
def activity_detail(request, board_no):
    if board_no is not None:
        context = {}
        board = Board.objects.get(pk=board_no)  # 게시글 번호로 게시글 내용을 들고옴
        context["board"] = board
        board_file_list = BoardFile.objects.filter(board_no=board)
        context["board_file_list"] = board_file_list
        comment_list = Comment.objects.filter(comment_board_no=board).filter(
            comment_cont_ref__isnull=True).order_by(
            'comment_created').prefetch_related('comment_set').all()  # 게시글 번호로 댓글 내용
        context["comment_list"] = comment_list
        return render(request, 'activity_detail.html', context)
    else:
        return redirect(reverse('activity'))


# 동아리 활동 등록하기
def activity_register(request):
    # 글쓰기 들어와서 등록 버튼을 누르면 실행이 되는 부분
    if request.method == "POST":
        if request.session.get("user_stu") is not None:
            activity = Board(  # 객체로 저장을 할 것이오
                board_type_no=BoardType.objects.get(pk=4),
                board_title=request.POST.get('board_title'),
                board_cont=request.POST.get('board_cont'),
                board_writer=User.objects.get(pk=request.session.get('user_stu'))  # 유저 학번 들고오는 것임
            )
            activity.save()  # DB 에 차곡차곡 저장을 함

            # ============================= 이미지 저장시키는 코드 =========================
            for updated_file in request.FILES.getlist("board_file"):
                # DB 저장
                new_board_file = BoardFile.objects.create(board_no=activity, board_file_path=updated_file)
                new_board_file.save()
            return redirect(reverse("activity"))
    return render(request, "activity_register.html", {})


# 동아리 글 수정 코드
def activity_update(request):
    # 수정을 누르면 GET 방식으로 DB 에 있는 것을 꺼내 온다.
    if request.method == "GET":
        board = Board.objects.get(pk=request.GET.get('board_no'))  # 맞는 것을 가져온다.
        board_file_list = BoardFile.objects.filter(board_no=board)
        context = {'board': board, 'board_file_list': board_file_list}
        print("board.board_writer.user_stu", board.board_writer.user_stu)
        if board.board_writer.user_stu == request.session.get("user_stu"):
            return render(request, 'activity_register.html', context)  # 이거로 보내줘서 작업 가능
        else:
            return redirect(reverse("activity"))

    # 수정을 하고 난 후 수정 버튼을 누를 경우 이걸로 진행 됌
    if request.method == 'POST':
        board = Board.objects.get(pk=request.POST.get('board_no'))  # 맞는 것을 가져온다.
        board_file_list = BoardFile.objects.filter(board_no=board)
        if board.board_writer.user_stu == request.session.get("user_stu"):
            board.board_title = request.POST.get('board_title')
            board.board_cont = request.POST.get('board_cont')
            board.save()
            # 이미 저장소에 있는 파일 순회
            for board_file in board_file_list:
                # exist_file_path_{파일id}가 없는 경우: 사용자가 기존에 있던 파일을 삭제하기로 결정하였음 (input tag가 없어지면서 값이 전송되지 않음)
                if request.POST.get("exist_file_path_" + str(board_file.board_file_id)) is None:
                    # 기존에 있던 저장소에 파일 삭제
                    os.remove(settings.MEDIA_ROOT + "/" + str(board_file.board_file_path))
                    # db 기록 삭제
                    board_file.delete()
            # 새로 사용자가 파일을 첨부한 경우
            for updated_file in request.FILES.getlist("board_file"):
                # DB 저장
                new_board_file = BoardFile.objects.create(board_no=board, board_file_path=updated_file)
                new_board_file.save()
                # 목록 페이지 이동 (수정 필요)
            return redirect(reverse("activity"))
    # 잘못 왔을 경우
    return render(request, 'activity_list.html', {})


# 동아리 활동 상세페이지에서 삭제하는 코드
def activity_delete(request):
    if request.method == "POST":  # 포스트로 넘어오는 경우
        board = Board.objects.get(pk=request.POST.get('board_no'))
        try:
            file_list = list(BoardFile.objects.filter(board_no=board))
            # file_list 라는 변수 선언 (여러개의 파일을 올릴 수 있으므로 list 로 변환)
            for i in range(len(file_list)):
                # file_list 의 크기 만큼 for 문으로 돌려서 파일 삭제 후 폴더 삭제
                os.remove('media/' + str(file_list[i].board_file_path))
            os.rmdir('media/board/' + str(board.board_no))
            # 파일이 안에 있는 삭제에서 폴더를 삭제할 경우 오류 만남.
        except FileNotFoundError:
            pass  # 파일이 없는 경우 그냥 통과시킨다.
        board.delete()  # 파일과 폴더 삭제 후, 게시글 DB 에서 삭제
        return redirect(reverse('activity'))

    else:  # 파라미터가 제대로 넘어오지 않은 경우, 즉 비정상적인 경로를 통해 들어간 경우 바로 나오게 해준다.
        return redirect(reverse('activity'))


# 댓글 달기 코드
def activity_comment_register(request):
    user_stu = User.objects.get(pk=request.session.get('user_stu'))  # 유저 학번 들고오는 것임
    if request.method == "POST":

        board_no = Board.objects.get(pk=request.POST.get('board_no'))  # 게시글 번호 들고오는 것임

        # 객체로 받아서 저장할 예정
        comment = Comment(  # 받은 정보로 덧글 생성
            comment_board_no=board_no,  # 해당 게시글에
            comment_writer=user_stu,  # 해당 학번이
            comment_cont=request.POST.get('comment_cont')  # 사용자가 쓴 내용을 가져옴
        )
        comment.save()
    else:
        board_no = Board.objects.get(pk=request.GET.get('board_no'))  # 게시글 번호 들고오는 것임
        # 객체로 받아서 저장할 예정
        comment = Comment(
            comment_board_no=board_no,
            comment_writer=user_stu,
            comment_cont=request.GET.get('comment_cont'),
            comment_cont_ref=Comment.objects.get(pk=request.GET.get("comment_ref"))
        )
        comment.save()
        # 데이터 베이스에 저장
    return HttpResponse(  # 게시글 상세 페이지로 다시 돌아감, 리다이렉트를 이용한 것은 실행 안해봄. 아마 이게 제일 정확하지 않을까 싶음.
        "<script>location.href='/activity/" + str(board_no.board_no) + "/detail/';</script>")  # 게시글 상세페이지로 이동


# 댓글 삭제 코드
def activity_comment_delete(request):
    board_no = request.POST.get("board_no")
    if request.method == "POST":  # 댓글 삭제를 누를 경우
        comment = Comment.objects.get(pk=request.POST.get('comment_id'))
        # 그 댓글의 pk 를 찾아서 DB 에서 지운다.
        comment.delete()
    return HttpResponse("<script>location.href='/activity/" + str(board_no) + "/detail/';</script>")  # 게시글 상세페이지로 이동


# 댓글 수정 코드
def activity_comment_update(request):
    if request.method == "POST":  # 정상적으로 파라미터가 넘어왔을 경우
        comment = get_object_or_404(Comment, pk=request.POST.get('comment_id'))  # 가져온 comment_id를 토대로 수정 내역을 적용
        comment.comment_cont = request.POST.get('comment_cont')  # 수정할 내용을 가져옴
        comment.save()  # DB 저장
        return HttpResponse(  # 게시글 상세 페이지로 돌아감
            "<script>location.href='/activity/" + str(comment.comment_board_no.board_no) + "/detail/';</script>")


def history_register(request):  # 연혁 등록
    if request.method == "POST":  # 정상적으로 값이 넘어왔을 경우
        history = History.objects.create(  # history 객체 생성 후 받은 값을 집어넣음.
            history_cont=request.POST.get("history_cont"),
            history_date=request.POST.get("history_date"),
            history_writer=User.objects.get(pk=request.session.get("user_stu"))
        )
        history.save()
        return redirect(reverse("introduce"))  # 소개 페이지로 리다이렉트
    else:  # 비 정상적인 경로로 접근하였을 경우 (해킹 시도)
        print("비정상적인 접근: ", request.session.get("user_stu"))
        return render(request, "index.html", {'lgn_is_failed': 1})


def history_update(request):  # 연혁 수정
    if request.method == "POST":  # 정상적으로 파라미터가 넘어왔을 경우
        history = History.objects.get(pk=request.POST.get("history_no"))  # 가져온 history_no를 토대로 수정 내역을 적용
        history.history_cont = request.POST.get("history_cont")
        history.history_date = request.POST.get("history_date")
        history.history_writer = User.objects.get(pk=request.session.get("user_stu"))
        history.save()
        return redirect(reverse("introduce"))
    else:  # 비정상적인 접근의 경우 (해킹시도)
        return render(request, "index.html", {'lgn_is_failed': 1})  # 메인페이지로 보내버림


def history_delete(request):  # 연혁 삭제
    if request.method == "POST":  # 정상적으로 파라미터가 넘어왔을 경우
        history = History.objects.get(pk=request.POST.get("history_no"))  # 가져온 history_no를 토대로 삭제할 대상을 가져옴
        history.delete()  # 삭제
        return redirect(reverse("introduce"))  # 소개 페이지로 리다이렉팅
    else:  # 비정상적인 접근의 경우(해킹시도)
        return render(request, "index.html", {'lgn_is_failed': 1})  # 메인페이지로 보내버림
