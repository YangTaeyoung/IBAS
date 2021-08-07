from django.contrib import messages
from DB.models import Lect, Board, LectBoard, ContestBoard, UserDelete
from django.shortcuts import redirect, reverse
import functools


# 에러메시지를 얻는 함수.
def get_error_message(request, name="게시글이"):
    messages.warning(request, f'해당 {name} 존재하지 않습니다. 삭제되었을 수 있습니다.')


### 각 인스턴스가 존재하는지 확인하고 존재하면 인스턴스를, 존재하지 않으면 에러메시지를 출력 후 리스트 페이지로 돌아가는 함수.

def exist_check(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if lect_no := kwargs.get("lect_no"):
            try:
                Lect.objects.get(pk=lect_no)
            except Lect.DoesNotExist:
                get_error_message(request, "강의가")
                return redirect("lect_view", type_no=1)
        elif lect_no := kwargs.get("room_no"):
            try:
                Lect.objects.get(pk=lect_no)
            except Lect.DoesNotExist:
                get_error_message(request, "강의가")
                return redirect("lect_view", type_no=1)
        elif lect_board_no := kwargs.get("lect_board_no"):
            try:
                LectBoard.objects.get(pk=lect_board_no)
            except LectBoard.DoesNotExist:
                get_error_message(request, "강의가")
                return redirect("lect_view", type_no=1)
        elif board_no := kwargs.get("board_no"):
            try:
                Board.objects.get(pk=board_no)
            except Board.DoesNotExist:
                get_error_message(request)
                return redirect("board_view", board_type_no=5)
        elif contest_no := kwargs.get("contest_no"):
            try:
                ContestBoard.objects.get(pk=contest_no)
            except ContestBoard.DoesNotExist:
                get_error_message(request)
                return redirect(reverse("contest_list"))
        elif activity_no := kwargs.get("activity_no"):
            try:
                board = Board.objects.get(pk=activity_no)
                if board.board_type_no.board_type_no != 4:
                    raise Board.DoesNotExist()
            except Board.DoesNotExist:
                get_error_message(request)
                return redirect(reverse("activity"))
        elif user_delete_no := kwargs.get("user_delete_no"):
            try:
                UserDelete.objects.get(pk=user_delete_no)
            except UserDelete.DoesNotExist:
                get_error_message(request, "제명 안건이")
                return redirect(reverse("staff_member_list"))

        return func(request, *args, **kwargs)

    return wrapper