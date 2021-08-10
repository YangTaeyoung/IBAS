from DB.models import Board, ContestBoard, LectBoard, Comment, UserDelete, Lect
from django.db.models import Q
from django.contrib import messages
import functools
from django.shortcuts import redirect
from user_controller import get_logined_user, is_superuser

# 인스턴스를 파악해 해당 인스턴스의 덧글을 지우는 함수. 게시글을 삭제할 때 사용.
# 2021-08-04.. board_ref => comment_board_ref 오류나서 바꿨습니다..
def comment_delete_by_post_delete(instance):
    comment_list = None
    if isinstance(instance, Board):
        board_ref = instance.board_no
        comment_list = Comment.objects.filter(Q(comment_board_ref=board_ref) & Q(comment_type_id=1))
    elif isinstance(instance, ContestBoard):
        board_ref = instance.contest_no
        comment_list = Comment.objects.filter(Q(comment_board_ref=board_ref) & Q(comment_type_id=2))
    elif isinstance(instance, LectBoard):
        board_ref = instance.lect_board_no
        comment_list = Comment.objects.filter(Q(comment_board_ref=board_ref) & Q(comment_type_id=3))
    elif isinstance(instance, UserDelete):
        board_ref = instance.user_delete_no
        comment_list = Comment.objects.filter(Q(comment_board_ref=board_ref) & Q(comment_type_id=4))
    if comment_list is not None:
        for comment in comment_list:
            comment.delete()


# 강의가 진행중인지 확인하는 것.
def is_ongoing(lect: Lect):
    return lect.lect_state_id == 3 or lect.lect_state_id == 1


# 데코레이터
# 회장단은 강의가 종강 후에도 강의실 내부에 들어갈 수 있어야 하므로 그 부분은 예외처리했음.
def ongoing_check(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        lect_no = kwargs.get('lect_no', kwargs.get('room_no', None))
        lect = Lect.objects.get(pk=lect_no)
        cur_user = get_logined_user(request)
        if is_ongoing(lect) or cur_user == lect.lect_chief or is_superuser(cur_user):
            return func(request, *args, **kwargs)
        else:
            if lect.lect_state_id == 2:
                messages.warning(request, "강의가 거절된 상태입니다. 입장할 수 없습니다.")
            else:
                messages.warning(request, "강의가 종료되었습니다.")
            return redirect("lect_view", type_no=lect.lect_type_id)
    return wrapper
