import functools
from django.shortcuts import redirect, reverse
from DB.models import User, ContestBoard, Board, Bank, Lect, LectBoard


# 로그인 했는지 여부를 반환하는 함수
def is_logined(request):
    return request.session.get("user_stu") is not None


# 관리자인지의 여부를 확인하는 함수
def is_superuser(request):
    current_user = get_logined_user(request)
    return current_user.user_role.role_no <= 3


# 글쓴이인지의 여부를 확인하는 함수
def is_writer(request, **kwargs):
    current_user = get_logined_user(request)
    board_no = kwargs.get('board_no')
    contest_no = kwargs.get('contest_no')
    bank_no = kwargs.get('bank_no')
    lect_no = kwargs.get('lect_no')
    # comment_no = kwargs.get('comment_no')

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


# 역할이 맞는지 확인 하는 함수
def role_check(request, role_no):
    return get_logined_user(request).user_role.role_no == role_no


#
# # 권한이 맞는지 확인하는 함수
# def auth_check(request, auth_no):
#     return get_logined_user(request).user_auth.auth_no == auth_no


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
# 작성자: 유동현
# 수정자: 양태영
# 현재 접속 중인 유저가 글쓴이인지 확인하는 함수, 글을 수정 및 삭제할 때 필요
# superuser=True 이면 관리자 모드. 관리자인 경우도 접근 허용
# superuser=False 이면 관리자도 접근 불가. 글쓴이만 접근 가능
# 수정내용: 체크 부분 모듈화로 코드 간결화
def writer_only(superuser=False):
    def decorator(func):
        @login_required
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            # 권한이 일치하지 않으면 메인페이지로 이동
            if superuser:
                if is_writer(request, **kwargs) or is_superuser(request):
                    return func(request, *args, **kwargs)
            else:
                if is_writer(request, **kwargs):
                    return func(request, *args, **kwargs)

            return redirect(reverse("index"))

        return wrapper

    return decorator


# 데코레이터
# 수정자:양태영
# 수정일시: 6월 16일
# 수정내용: 총무 권한을 추가할지 추가하지 않을지 결정하는 함수. True일 경우 총무여도 권한 허용.
# 관리자 권한이 있는지 확인하는 함수
def superuser_only(cfo_included=False):
    def decorator(func):
        @login_required
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            current_user = get_logined_user(request)
            flag = 3
            if cfo_included:
                flag = 4
            if current_user.user_role.role_no <= flag:
                return func(request, *args, **kwargs)
            else:
                return redirect(reverse("index"))

        return wrapper

    return decorator


# 데코레이터
# 총무 권한이 있는지 확인하는 함수
def cfo_only(func):
    @login_required
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        current_user = get_logined_user(request)

        if current_user.user_role.role_no == 4:
            return func(request, *args, **kwargs)

        else:
            return redirect(reverse("index"))

    return wrapper


# 데코레이터
# 사용자 권한을 확인하는 함수(활동회원 or 비활동회원)
# 전체 회원 중 일원인지만 확인할 경우: active=False
# 납입 회원인지 확인할 경우: active=True
def auth_check(active=False):
    def decorator(func):
        @login_required
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            current_user = get_logined_user(request)
            if active:
                boundary = current_user.user_auth.auth_no == 1
            else:
                boundary = current_user.user_auth.auth_no <= 2

            if boundary:
                return func(request, *args, **kwargs)
            else:
                return redirect(reverse("index"))

        return wrapper

    return decorator
