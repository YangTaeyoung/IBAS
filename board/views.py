from django.shortcuts import render
from django.http import HttpResponse
from DB.models import Board, BoardFile, BoardType, User, UserRole, UserAuth
from django.db.models import Q, Count
from addr_handling import go_board, go_board_detail
from file_controller import is_image
from django.core.paginator import Paginator


def board_view(request, board_type_no):  # 게시판 페이지로 이동
    if board_type_no == 5:
        board_list = Board.objects.all().select_related("board_writer").order_by(
            "board_type_no__board_type_no").order_by("-board_created")
    else:
        board_list = Board.objects.filter(board_type_no=BoardType.objects.get(pk=board_type_no)).select_related(
            "board_writer").order_by("-board_created")

    paginator = Paginator(board_list, 10)  # 페이지네이터로 10개씩 보이게끔. 나중에 수정하면 됌
    page = request.GET.get('page')  # 페이지 이름 ㅇㅇ 여기서 변경하면 됌
    item = paginator.get_page(page)
    context = {
        "board_len": len(item),
        "message": "게시글이 존재하지 않습니다.",
        "board_list": item,
        "board_name": BoardType.objects.get(pk=board_type_no).board_type_name,
        "board_exp": BoardType.objects.get(pk=board_type_no).board_type_exp,
        "board_type_no": board_type_no,
        "all_num": Board.objects.all().count(),
        "notice_num": Board.objects.filter(board_type_no__board_type_no=1).count(),
        "free_num": Board.objects.filter(board_type_no__board_type_no=2).count(),
        "quest_num": Board.objects.filter(board_type_no__board_type_no=3).count(),
        "activity_num": Board.objects.filter(board_type_no__board_type_no=4).count()
    }
    return render(request, 'board.html', context)


def board_search(request):
    if request.method == "GET":
        keyword = request.GET.get("keyword")
        board_list = Board.objects.filter(
            Q(board_cont__icontains=keyword) | Q(board_title__icontains=keyword) | Q(
                board_writer__user_name=keyword)).select_related("board_writer").order_by("-board_created").all()

        paginator = Paginator(board_list, 10)  # 페이지네이터로 10개씩 보이게끔. 나중에 수정하면 됌
        page = request.GET.get('page')  # 페이지 이름 ㅇㅇ 여기서 변경하면 됌
        item = paginator.get_page(page)

        context = {
            "board_len": len(item),
            "message": "\"" + keyword + "\"로 검색한 게시글이 존재하지 않습니다.",
            "board_list": item,
            "board_name": "검색결과",
            "board_exp": keyword + "로 검색한 결과입니다.",
            "all_num": Board.objects.all().count(),
            "notice_num": Board.objects.filter(board_type_no__board_type_no=1).count(),
            "free_num": Board.objects.filter(board_type_no__board_type_no=2).count(),
            "quest_num": Board.objects.filter(board_type_no__board_type_no=3).count(),
            "activity_num": Board.objects.filter(board_type_no__board_type_no=4).count()
        }
        return render(request, "board.html", context)
    else:
        return HttpResponse(go_board(5))


def board_detail(request, board_no):
    board = Board.objects.get(pk=board_no)
    board_img_list = list()
    board_file_list = list()
    for board_file in BoardFile.objects.filter(board_no=board):
        if is_image(board_file.board_file_path):
            board_img_list.append(board_file)
        else:
            board_file_list.append(board_file)

    context = {
        "board": board,
        "board_file_list": board_file_list,
        "board_img_list": board_img_list
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
            new_board_file = BoardFile.objects.create(board_no=Board.objects.get(pk=board.board_no),
                                                      board_file_path=updated_file,
                                                      board_file_name=str(updated_file).rsplit("/")[0])
            new_board_file.save()
        return HttpResponse(go_board_detail(board.board_no))

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
    return render(request, 'activity_register.html', {})
