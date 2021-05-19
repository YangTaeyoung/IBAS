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


def is_writer(request, **kwargs):
    current_user = get_logined_user(request)

    board_no = kwargs.get('board_no')
    contest_no = kwargs.get('contest_no')
    bank_no = kwargs.get('bank_no')
    lect_no = kwargs.get('lect_no')

    # 글쓴이인가요
    if board_no is not None:
        board = Board.objects.get(pk=board_no)
        if current_user == board.board_writer:
            return True
    elif contest_no is not None:
        contest = ContestBoard.objects.get(pk=contest_no)
        if current_user == contest.contest_writer:
            return True
    elif lect_no is not None:
        lect = Lect.objects.get(pk=lect_no)
        if current_user == lect.lect_chief:
            return True
    elif bank_no is not None:
        bank = Bank.objects.get(pk=bank_no)
        if current_user == bank.bank_used_user:
            return True
    else:
        return False


# 작성자: 양태영
# 최종 수정일: 2021.5.19
# 내용: 로그인한 유저가 관리자인지 확인하는 함수 맞다면 True 반환 일반 게시판, 공모전게시판, 강의 게시판 등에서 관리자 판단용으로 사용
def is_superuser(request):
    current_user = get_logined_user(request)
    if current_user.user_role <= 3 and current_user.user_auth.auth_no == 1:
        return True
    return False


# 작성자: 양태영
# 최종 수정일: 2021.5.19
# 내용: 로그인한 유저가 총무인지 확인하는 함수 맞다면 True 반환, 예산신청 게시판, 예산 공시란 등에서 총무 판단용으로 사용됨.
def is_cfo(request):
    current_user = get_logined_user(request)
    if current_user.user_role == 4 and current_user.user_auth.auth_no == 1:
        return True
    return False


# 작성자: 유동현
# 수정자: 양태영
# 최종 수정일: 2021.05.19
# 함수종류: 데코레이터용
# 내용: 현재 접속 중인 유저가 글쓴이인지 확인하는 함수, 글을 수정할 때 필요
# superuser=True 이면 관리자 모드. 관리자인 경우도 접근 허용
# superuser=False 이면 관리자도 접근 불가. 글쓴이만 접근 가능
def writer_only(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        # 권한이 일치하지 않으면 메인페이지로 이동
        if is_writer(request, **kwargs):
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse("index"))

    return wrapper


# 작성자: 양태영
# 최종 수정일: 2021.05.19
# 함수 종류: 데코레이터
# 내용: 현재 접속중인 유저가 글쓴이, 혹은 관리자인지 확인하는 함수, 글을 삭제할 때 사용
def writer_or_superuser_only(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if is_writer(request, **kwargs) or is_superuser(request):
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse("index"))

    return wrapper


# 작성자: 양태영
# 최종 수정일: 2021.05.19
# 함수 종류: 데코레이터
# 내용: 현재 접속중인 유저가 글쓴이, 혹은 총무인지 확인하는 함수, 글을 삭제할 때 사용
def writer_or_cfo_only(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if is_writer(request, **kwargs) or is_cfo(request):
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
