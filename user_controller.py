import functools

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, reverse
from DB.models import User, ContestBoard, Board, Bank, Lect, LectBoard


# 로그인 했는지 여부를 반환하는 함수
def is_logined(request):
    return request.session.get("user_stu") is not None


# 역할이 맞는지 확인 하는 함수
def role_check(request, role_no):
    return get_logined_user(request).user_role.role_no == role_no


# 권한이 맞는지 확인하는 함수
def auth_check(request, auth_no):
    return get_logined_user(request).user_auth.auth_no == auth_no


# 유저 관련 객체를 반환하는 컨트롤러
def get_logined_user(request):  # 로그인한 유저 객체 반환
    return User.objects.get(pk=request.session.get("user_stu"))


# 학번을 넣어서 조회할 경우
def get_user(user_stu):
    return User.objects.get(pk=user_stu)


# post를 사용해서 일반적으로 받아온 경우
def get_user_post(request):
    return User.objects.get(pk=request.POST.get("user_stu"))


# get를 사용해서 일반적으로 받아온 경우
def get_user_get(request):
    return User.objects.get(pk=request.GET.get("user_stu"))


# 데코레이터
# 로그인 안한 유저가 접근시 메인페이지로 이동
def login_required(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if is_logined(request):
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse("index"))
    return wrapper


# 데코레이터
# 현재 접속 중인 유저가 글쓴이인지 확인하는 함수, 글을 수정 및 삭제할 때 필요
# superuser=True 이면 관리자 모드. 관리자인 경우도 접근 허용
# superuser=False 이면 관리자도 접근 불가. 글쓴이만 접근 가능
def writer_only(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        is_writer = False  # 현재 접속 중인 유저와 글쓴이가 일치하면 True
        current_user = User.objects.get(pk=request.session.get("user_stu"))

        board_no = kwargs.get('board_no')
        contest_no = kwargs.get('contest_no')

        # 글쓴이인가요
        if board_no is not None:
            board = Board.objects.get(pk=board_no)
            if current_user == board.board_writer:
                is_writer = True

        elif contest_no is not None:
            contest = ContestBoard.objects.get(pk=contest_no)
            if current_user == contest.contest_writer:
                is_writer = True
        else:
            pass

        # 권한이 일치하지 않으면 메인페이지로 이동
        if is_writer:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse("index"))

    return wrapper


# def writer_only(superuser=False):
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(request, *args, **kwargs):
#             # if not is_logined(request):
#             #     return redirect(reverse("index"))
#
#             is_writer = False  # 현재 접속 중인 유저와 글쓴이가 일치하면 True
#             is_superuser = False  # 삭제 권한을 가진 관리자이면 True
#             current_user = User.objects.get(pk=request.session.get("user_stu"))
#
#             board_no = kwargs.get('board_no')
#             contest_no = kwargs.get('contest_no')
#
#             # 글쓴이인가요
#             if board_no is not None:
#                 board = Board.objects.get(pk=board_no)
#                 if current_user == board.board_writer:
#                     is_writer = True
#
#             elif contest_no is not None:
#                 contest = ContestBoard.objects.get(pk=contest_no)
#                 if current_user == contest.contest_writer:
#                     is_writer = True
#             else:
#                 pass
#
#             # 관리자 모드
#             if superuser:
#                 if current_user.user_role.role_no <= 3:
#                     is_superuser = True
#
#             # 권한이 일치하지 않으면 메인페이지로 이동
#             if is_writer or is_superuser:
#                 return func(request, *args, **kwargs)
#             else:
#                 return redirect(reverse("index"))
#
#         return wrapper
#     return decorator
