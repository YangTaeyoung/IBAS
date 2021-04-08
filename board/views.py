import datetime
from datetime import date

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from DB.models import Board, BoardFile, BoardType, User, UserRole, UserAuth, Comment, ContestBoard, ContestFile
from django.db.models import Q, Count
from addr_handling import go_board, go_board_detail
from file_controller import is_image
from django.core.paginator import Paginator
from django.conf import settings
import os


def get_sidebar_information():
    return {
        "all_num": Board.objects.all().count(),
        "notice_num": Board.objects.filter(board_type_no__board_type_no=1).count(),
        "free_num": Board.objects.filter(board_type_no__board_type_no=2).count(),
        "quest_num": Board.objects.filter(board_type_no__board_type_no=3).count(),
        "activity_num": Board.objects.filter(board_type_no__board_type_no=4).count(),
        "contest_num": ContestBoard.objects.all().count(),
    }


def get_page_object(request, board_list, num_of_boards_in_one_page=10):
    paginator = Paginator(board_list, num_of_boards_in_one_page)  # 페이지네이터로 10개씩 보이게끔. 나중에 수정하면 됌
    page = request.GET.get('page')  # 페이지 이름 ㅇㅇ 여기서 변경하면 됌
    item = paginator.get_page(page)

    return item


def board_view(request, board_type_no):  # 게시판 페이지로 이동
    if board_type_no == 5:
        board_list = Board.objects.all().select_related("board_writer").order_by(
            "board_type_no").order_by("-board_created")
    else:
        board_list = Board.objects.filter(board_type_no=BoardType.objects.get(pk=board_type_no)).select_related(
            "board_writer").order_by("-board_created")

    item = get_page_object(request, board_list)
    context = {
        "board_len": len(item),
        "message": "게시글이 존재하지 않습니다.",
        "board_list": item,
        "board_name": BoardType.objects.get(pk=board_type_no).board_type_name,
        "board_exp": BoardType.objects.get(pk=board_type_no).board_type_exp,
        "board_type_no": board_type_no,
    }
    context.update(get_sidebar_information())

    return render(request, 'board.html', context)


def board_search(request):
    if request.method == "GET":
        keyword = request.GET.get("keyword")
        board_list = Board.objects.filter(
            Q(board_cont__icontains=keyword) | Q(board_title__icontains=keyword) | Q(
                board_writer__user_name=keyword)).select_related("board_writer").order_by("-board_created").all()

        item = get_page_object(request, board_list)
        context = {
            "board_len": len(item),
            "message": "\"" + keyword + "\"로 검색한 게시글이 존재하지 않습니다.",
            "board_list": item,
            'board_type_no': 5,
            "board_name": "검색결과",
            "board_exp": keyword + "로 검색한 결과입니다.",
        }
        context.update(get_sidebar_information())

        return render(request, "board.html", context)
    else:
        return HttpResponse(go_board(5))


def board_detail(request, board_no):  # 게시글 상세 보기
    board = Board.objects.get(pk=board_no)  # 게시글을 불러옴
    board_img_list = list()  # 이미지를 담을 리스트
    board_file_list = list()  # 이미지가 아닌 파일을 담는 리스트
    for board_file in BoardFile.objects.filter(board_no=board):  # DB 파일 리스트 순회
        if is_image(board_file.board_file_path):  # 파일이 이미지이면
            board_img_list.append(board_file)  # 이미지 리스트에 저장
        else:  # 이미지가 아니면
            board_file_list.append(board_file)  # 파일 리스트에 저장

    comment_list = Comment.objects.filter(comment_board_no=board).order_by("-comment_created").prefetch_related(
        "comment_set")

    context = {
        "board": board,
        "board_file_list": board_file_list,
        "board_img_list": board_img_list,
        "img_len": len(board_img_list),
        "file_len": len(board_file_list),
        "comment_list": comment_list
    }
    return render(request, 'board_detail.html', context)


def board_register(request):
    # 글쓰기 들어와서 등록 버튼을 누르면 실행이 되는 부분
    if request.method == "POST":
        board = Board(  # 객체로 저장을 할 것이오
            board_type_no=BoardType.objects.get(pk=request.POST.get("board_type_no")),
            board_title=request.POST.get('board_title'),
            board_cont=request.POST.get('board_cont'),
            board_writer=User.objects.get(pk=request.session.get('user_stu'))  # 유저 학번 들고오는 것임
        )
        board.save()  # DB 에 차곡차곡 저장을 함

        # ============================= 이미지 저장시키는 코드 =========================
        for updated_file in request.FILES.getlist("board_file"):
            # DB 저장
            new_board_file = BoardFile(board_no=Board.objects.get(pk=board.board_no),
                                       board_file_path=updated_file,
                                       board_file_name=str(updated_file)[str(updated_file).rfind("/") + 1:])
            new_board_file.save()

        return redirect("board_detail", board_no=board.board_no)

    else:  # 게시글 등록 버튼을 눌렀을 때
        board_type_no = request.GET.get("board_type_no")
        context = {
            "board_type_no": board_type_no,
            "board_name": BoardType.objects.get(pk=board_type_no).board_type_name,
            "board_exp": BoardType.objects.get(pk=board_type_no).board_type_exp,
        }
        return render(request, "board_register.html", context)


def board_update(request):
    # POST가 아닌 그냥 보여주는 방식
    # 수정을 누르면 GET 방식으로 DB 에 있는 것을 꺼내 온다.
    if request.method == "GET":
        board = Board.objects.get(pk=request.GET.get('board_no'))  # 맞는 것을 가져온다.
        board_file_list = BoardFile.objects.filter(board_no=board)
        context = {
            'board': board,
            'board_file_list': board_file_list,
            "board_type_no": board.board_type_no.board_type_no,
            "board_name": board.board_type_no.board_type_name,
            "board_exp": board.board_type_no.board_type_exp,
        }

        if board.board_writer.user_stu == request.session.get("user_stu"):
            return render(request, 'board_register.html', context)  # 이거로 보내줘서 작업 가능
        else:
            return redirect("board_view", board_type_no=board.board_type_no.board_type_no)

    # 수정을 하고 난 후 수정 버튼을 누를 경우 이걸로 진행 됌
    else:
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
                new_board_file = BoardFile.objects.create(board_no=board, board_file_path=updated_file,
                                                          board_file_name=str(updated_file)[
                                                                          str(updated_file).rfind("/") + 1:])
                new_board_file.save()
                # 목록 페이지 이동 (수정 필요)
            return redirect("board_detail", board_no=board.board_no)
        else:  # 다른 사람이 임의로 게시글을 수정하려 시도하는 경우(해킹 시도)
            return redirect("board_view", board_type_no=board.board_type_no.board_type_no)


# 게시글 상세페이지에서 삭제하는 코드
def board_delete(request):
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
        return redirect('board_view', board_type_no=5)

    else:  # 파라미터가 제대로 넘어오지 않은 경우, 즉 비정상적인 경로를 통해 들어간 경우 바로 나오게 해준다.
        return redirect('board_view', board_type_no=5)


# 댓글 달기 코드
def board_comment_register(request):
    if request.method == "POST":

        board_no = Board.objects.get(pk=request.POST.get('board_no'))  # 게시글 번호 들고오는 것임

        # 객체로 받아서 저장할 예정
        comment = Comment(  # 받은 정보로 덧글 생성
            comment_board_no=board_no,  # 해당 게시글에
            comment_writer=User.objects.get(pk=request.session.get('user_stu')),  # 해당 학번이
            comment_cont=request.POST.get('comment_cont')  # 사용자가 쓴 내용을 가져옴
        )
        comment.save()
    else:
        board_no = Board.objects.get(pk=request.GET.get('board_no'))  # 게시글 번호 들고오는 것임
        # 객체로 받아서 저장할 예정
        comment = Comment(
            comment_board_no=board_no,
            comment_writer=User.objects.get(pk=request.session.get('user_stu')),
            comment_cont=request.GET.get('comment_cont'),
            comment_cont_ref=Comment.objects.get(pk=request.GET.get("comment_ref"))
        )
        comment.save()
        # 데이터 베이스에 저장
    return HttpResponse(  # 게시글 상세 페이지로 다시 돌아감, 리다이렉트를 이용한 것은 실행 안해봄. 아마 이게 제일 정확하지 않을까 싶음.
        "<script>location.href='/activity/" + str(board_no.board_no) + "/detail/';</script>")  # 게시글 상세페이지로 이동


# 댓글 삭제 코드
def board_comment_delete(request):
    if request.method == "POST":  # 댓글 삭제를 누를 경우
        comment = Comment.objects.get(pk=request.POST.get('comment_id'))
        board_type_no = comment.comment_board_no.board_type_no.board_type_no
        # 그 댓글의 pk 를 찾아서 DB 에서 지운다.
        comment.delete()
        return HttpResponse(go_board(board_type_no))  # 게시글 상세페이지로 이동
    else:
        return HttpResponse(go_board(5))  # 잘못 들어온 접근은 전체 게시판으로 이동


# 댓글 수정 코드
def board_comment_update(request):
    if request.method == "POST":  # 정상적으로 파라미터가 넘어왔을 경우
        comment = Comment.objects.get(pk=request.POST.get('comment_id'))  # 가져온 comment_id를 토대로 수정 내역을 적용
        comment.comment_cont = request.POST.get('comment_cont')  # 수정할 내용을 가져옴
        comment.save()  # DB 저장
        return HttpResponse(go_board_detail(comment.comment_board_no.board_no))  # 게시글 상세 페이지로 돌아감
    else:
        return HttpResponse(go_board(5))  # 잘못된 요청의 경우 전체 게시판으로 이동하게 함.


def contest_list(request):  # 게시판 페이지로 이동
    contest_board_list = ContestBoard.objects.all().order_by('-contest_deadline').prefetch_related("contestfile_set")

    item = get_page_object(request, contest_board_list, num_of_boards_in_one_page=6)

    context = {
        "board_len": len(item),
        "message": "아직 등록한 공모전이 없습니다.",
        "contest_list": item,
        "board_name": "공모전 게시판",  # BoardType.objects.get(pk=6).board_type_name,
        "board_exp": "공모전 정보를 알려주는 게시판",  # BoardType.objects.get(pk=6).board_type_exp,
    }
    context.update(get_sidebar_information())

    return render(request, 'contest_board.html', context)


def contest_register(request):

    if request.method == 'POST':

        contest = ContestBoard(
            contest_title=request.POST.get('contest_title'),
            contest_asso=request.POST.get('contest_asso'),
            contest_start=date.fromisoformat(request.POST.get('contest_start')), # %Y-%m-%d 15:00:00,
            contest_deadline=date.fromisoformat(request.POST.get('contest_deadline')), # %Y-%m-%d 15:00:00,
            contest_topic=request.POST.get('contest_topic'),
            contest_cont=request.POST.get('contest_cont'),
            contest_writer=User.objects.get(pk=request.session['user_stu']),
        )
        contest.save()

        if "contest_file" in request.FILES:
            for file in request.FILES.getlist("contest_file"):
                ContestFile.objects.create(
                    contest_no=ContestBoard.objects.get(pk=contest.contest_no),
                    contest_file_path=file, # imageField 객체 <- uploadedFile 객체 할당
                    contest_file_name=file.name
                )

    elif request.method == 'GET':
        return render(request,'contest_register.html')

    return redirect(reverse('contest_list'))


def contest_detail(request):  # 게시판 상세 페이지로 이동
    return render(request, 'contest_detail.html', {})
