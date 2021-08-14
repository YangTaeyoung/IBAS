from DB.models import Board, ContestBoard, LectBoard, Comment, UserDelete, Lect
from django.db.models import Q
from django.contrib import messages
import functools
from django.shortcuts import redirect
from DB.models import User

##############################################################
# 게시글, 강의, 제명건의 등 유저와는 관련이 없는 오브젝트를 다룰 때 사용하는 컨트롤러.
##############################################################

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


# 제작: 양태영
# 제작일: 21-08-11
# 내용 강의가 진행중인지 확인하는 함수
# input: 확인할 강의 객체
# output: 대기중, 혹은 강의 승인 상태일 경우 true/거절, 종료 상태일 경우 false
def is_ongoing(lect: Lect):
    return lect.lect_state_id == 3 or lect.lect_state_id == 1


# 제작: 양테영
# 제작일: 21-08-11
# 제작 내용: 강의가 진행중인지를 확인하는 데코레이터, 강의가 진행중이라면 강의실에 입장 가능하게 하기 위해 만듦.
# 회장단은 강의가 종강 후에도 강의실 내부에 들어갈 수 있어야 하므로 그 부분은 예외처리했음.
def ongoing_check(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        lect_no = kwargs.get('lect_no', kwargs.get('room_no', None))
        lect = Lect.objects.get(pk=lect_no)
        cur_user = User.objects.get(pk=request.session.get("user_stu"))
        # 강의가 진행중이거나, 강의자이거나, 운영진의 경우 강의실에 입장 가능
        if is_ongoing(lect) or cur_user == lect.lect_chief or cur_user.user_role_id <= 3:
            return func(request, *args, **kwargs)
        else:  # 종강하였으며, 일반회원일 경우.
            if lect.lect_state_id == 2:  # 상태: 거절
                messages.warning(request, "강의가 거절된 상태입니다. 입장할 수 없습니다.")
            else:  # 상태: 종료
                messages.warning(request, "강의가 종료되었습니다.")
            return redirect("lect_view", type_no=lect.lect_type_id)

    return wrapper
