import functools
from django.shortcuts import redirect, reverse
from DB.models import User, ContestBoard, Board, Bank, Lect, UserDelete, AuthUser
from allauth.socialaccount.models import SocialAccount, SocialToken


# 학교 아이디의 경우 이름/학과/학교 등으로 이름이 구성된 경우가 많음.
# 그 경우 앞부분을 잘라주는 함수임.
def get_real_name(name_str: str):
    real_name = name_str
    idx_slash = name_str.find("/")
    if idx_slash != -1:
        real_name = name_str.split("/")[0]
    return real_name


# 소셜로그인으로부터 정보를 얻어오는 함수임
def get_social_login_info(password):
    auth_user = AuthUser.objects.filter(password=password).first()
    # 있다면 social account에서 앞서서 Auth의 primary key를 통해 가입한 친구의 pk를 넣어서 조회
    tar_member = SocialAccount.objects.filter(user_id=auth_user.id).first()  # quesyset의 첫번째 자료. 즉 로그인한 인원의 인스턴스 변수
    tar_token = SocialToken.objects.filter(account_id=tar_member.id).first()
    social_login_info_dict = dict()

    # extra_data: 사용자의 동의를 통해 로그인 출처로 부터 얻은 사용자의 개인정보
    social_login_info_dict["email"] = tar_member.extra_data.get('email')  # 자동 완성을 위해 인스턴스 변수 설정
    social_login_info_dict["name"] = get_real_name(tar_member.extra_data.get('name'))  # 자동 완성을 위한 이름 설정
    social_login_info_dict["provider"] = tar_member.provider
    if social_login_info_dict["provider"] == "google":  # 사용자가 구글을 통해 로그인 한 경우
        social_login_info_dict["pic"] = tar_member.extra_data.get('picture')  # extra_data 테이블에서 꺼내는 변수를 picture로 설정
    elif social_login_info_dict["provider"] == "naver":  # 사용자가 네이버를 통해 로그인 한 경우
        social_login_info_dict["pic"] = tar_member.extra_data.get(
            'profile_image')  # extra_data 테이블에서 꺼내는 변수를 profile_image로 설정

    # 소셜 로그인으로 부터 받은 정보는 저장하지 않기 위해 해당 정보 삭제
    tar_token.delete()
    tar_member.delete()
    auth_user.delete()

    return social_login_info_dict


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
    user_delete_no = kwargs.get('user_delete_no')

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
    elif user_delete_no is not None:
        user_delete = UserDelete.objects.get(pk=user_delete_no)
        if current_user == user_delete.suggest_user:
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


# 데코레이터
# 제작일: 21.6.21 15.43
# 제작자: 양태영
# 용도: 회장인지 아닌지 판별하는 데코레이터 vice가 True 일 경우 부화장인지 봄
def chief_only(vice=False):
    def decorator(func):
        @login_required
        @auth_check(True)
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            current_user = get_logined_user(request)
            if vice and current_user.user_role.role_no <= 2:
                return func(request, *args, **kwargs)
            elif not vice and current_user.user_role.role_no == 1:
                return func(request, *args, **kwargs)
            else:
                return redirect(reverse("index"))

        return wrapper

    return decorator
