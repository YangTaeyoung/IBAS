import functools
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, reverse, render
from DB.models import User, ContestBoard, Board, Bank, Lect, UserDelete, AuthUser, History, LectEnrollment, \
    LectBoard, Answer, UserEmail, Comment, LectAssignmentSubmit, Alarm, PolicyTerms, LectAttendance
from allauth.socialaccount.models import SocialAccount, SocialToken
from file_controller import FileController
from django.db.models import Q
from django.db import transaction
from post_controller import comment_delete_by_post_delete


def is_professor(cur_user: User):
    return cur_user.user_role_id == 5


# 디폴트 유저의 정보를 가져옴.
def get_default_user():
    return User.objects.get(pk=0)


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
def is_superuser(cur_user, is_bank=False):
    if is_bank:
        return role_check(cur_user, 4, "equal")
    else:
        return role_check(cur_user, 3, "lte")


# 강의자 여부 확인 함수
def is_lect_instructor(cur_user, **kwargs):
    lect_no = kwargs.get('lect_no', kwargs.get('room_no', None))

    if lect_no is not None and cur_user == Lect.objects.get(pk=lect_no).lect_chief:
        return True
    if lect_no is None:
        print('강의를 확인할 수 없습니다, is lect instructor 확인바람')
    return False


# 글쓴이인지의 여부를 확인하는 함수
def is_writer(cur_user, **kwargs):
    board_no = kwargs.get('board_no')
    contest_no = kwargs.get('contest_no')
    bank_no = kwargs.get('bank_no')
    lect_no = kwargs.get('lect_no', kwargs.get('room_no'))
    user_delete_no = kwargs.get('user_delete_no')
    assignment_submit_no = kwargs.get('submit_no')  # 수강생 과제 제출
    comment_id = kwargs.get('comment_id')

    # 글쓴이인가요
    if board_no is not None:
        board = Board.objects.get(pk=board_no)
        if cur_user == board.board_writer:
            return True
    elif contest_no is not None:
        contest = ContestBoard.objects.get(pk=contest_no)
        if cur_user == contest.contest_writer:
            return True
    elif assignment_submit_no is not None:
        assignment = LectAssignmentSubmit.objects.get(pk=assignment_submit_no)
        if cur_user == assignment.assignment_submitter:
            return True
    elif lect_no is not None:
        lect = Lect.objects.get(pk=lect_no)
        if cur_user == lect.lect_chief:
            return True
    elif bank_no is not None:
        bank = Bank.objects.get(pk=bank_no)
        if cur_user == bank.bank_used_user:
            return True
    elif user_delete_no is not None:
        user_delete = UserDelete.objects.get(pk=user_delete_no)
        if cur_user == user_delete.suggest_user:
            return True
    elif comment_id is not None:
        comment = Comment.objects.get(pk=comment_id)
        if cur_user == comment.comment_writer:
            return True
    else:
        return False


# 역할이 맞는지 확인 하는 함수
# 입력: request, 기준이 될 역할 번호, 검증할 부등호
# 출력: 로그인 한 유저가 해당 조건에 만족하는지의 여부를 반환
def role_check(cur_user, role_no, sign="equal"):
    if sign == "equal":  # 등호
        return cur_user.user_role.role_no == role_no
    elif sign == "lte":  # 이하
        return cur_user.user_role.role_no <= role_no
    elif sign == "gte":  # 이상
        return cur_user.user_role.role_no >= role_no
    elif sign == "lt":  # 미만
        return cur_user.user_role.role_no < role_no
    elif sign == "gt":  # 초과
        return cur_user.user_role.role_no > role_no


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


# 작성자: 유동현
# 작성일시 : 2021.07.14
# 잘못된 접근시 메인페이지로 이동시킴
# msg 에 메세지를 적으면, 메인페이지에서 alert 창으로 경고를 띄움 (default msg = '접근 권한이 없습니다.')
# 차라리 조용히 404 페이지를 띄워주는것도 좋을거같고..? => 해당 url 이 존재하는지 외부로부터 감출 수 있음
# 수정자: 양태영
# 수정일자: 21.07.29
# 수정내용: next_url 파라미터를 추가, 입력하지 않으면 디폴트로 index로 이동하며 추가로 입력할 경우 해당 url로 이동함.
def not_allowed(request, msg="접근 권한이 없습니다.", error_404=False, next_url="index"):
    if error_404:
        raise Http404
    else:
        messages.warning(request, msg)  # 메인에서 alert 창 띄우기
        return redirect(next_url)


# 데코레이터
# 로그인 안한 유저가 접근시 메인페이지로 이동
def login_required(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if is_logined(request):
            return func(request, *args, **kwargs)
        else:
            return not_allowed(request, msg='로그인이 필요합니다!', next_url="login")

    return wrapper


# 데코레이터
# 작성자: 유동현
# 수정자: 양태영
# 현재 접속 중인 유저가 글쓴이인지 확인하는 함수, 글을 수정 및 삭제할 때 필요
# superuser=True 이면 관리자 모드. 관리자인 경우도 접근 허용
# superuser=False 이면 관리자도 접근 불가. 글쓴이만 접근 가능
# 수정내용: 체크 부분 모듈화로 코드 간결화
# 추가 수정 (2021-08-04) is_writer/is_superuser 내부의 get_logined_user 제거, 쿼리 발생 줄임
def writer_only(superuser=False, is_lect_assignment=False):
    def decorator(func):
        @login_required
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            # 권한이 일치하지 않으면 메인페이지로 이동
            cur_user = get_logined_user(request)
            if superuser:
                # 예산 지원 신청의 경우 총무가 삭제해야 함. 관리자 권한을 일반 운영팀이 아닌 총무로 할당.
                if kwargs.get("bank_no") and is_superuser(cur_user, is_bank=True):
                    return func(request, *args, **kwargs)
                # 예산 지원 신청이 아닌 경우.
                if is_writer(cur_user, **kwargs) or is_superuser(cur_user):
                    return func(request, *args, **kwargs)

            elif is_lect_assignment:
                # lect.views.lect_assignment_detail 에서만 사용됨.
                # 과제 작성자 본인이거나 / 운영팀이거나 / 강의자 => 수강생이 제출한 과제 열람 가능
                if is_writer(cur_user, **kwargs) or is_superuser(cur_user) or is_lect_instructor(cur_user, **kwargs):
                    return func(request, *args, **kwargs)

            else:
                if is_writer(cur_user, **kwargs):
                    return func(request, *args, **kwargs)

            return not_allowed(request)

        return wrapper

    return decorator


# 데코레이터
# 작성자: 유동현
# 2021.08.04
# 현재 접속 중인 유저가 강의자인지 확인하는 함수
def instructor_only(superuser=False):
    def decorator(func):
        @login_required
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            # 권한이 일치하지 않으면 메인페이지로 이동
            cur_user = get_logined_user(request)

            if superuser:
                # 운영팀은 강의자 메뉴 열람만 가능 / 정보 변경 불가
                if is_lect_instructor(cur_user, **kwargs) or (is_superuser(cur_user) and request.method == "GET"):
                    return func(request, *args, **kwargs)
                elif request.method == "POST":  # 권한 없는 사람(운영팀)이 정보 수정 시도 시, 현재 url 페이지 리다이렉트
                    return not_allowed(request, next_url=request.path)

            if is_lect_instructor(cur_user, **kwargs):
                return func(request, *args, **kwargs)

            return not_allowed(request, error_404=True)

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
                return not_allowed(request, error_404=True)

        return wrapper

    return decorator


# 제작: 양태영
# 제작일: 21-08-04
# 제작 내용: 교수의 입장을 제한하는 데코레이터
def prohibit_professor(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        cur_user = get_logined_user(request)
        if is_professor(cur_user):
            return not_allowed(request)
        return func(request, *args, **kwargs)

    return wrapper


# 제작: 양태영
# 제작 내용: 일반회원 입장에서, 강의에 등록이 가능한지 확인하는 데코레이터, 강의 인원이 가득찼거나, 강의 모집기간이 만료된 경우 False를 출력 
# INPUT: 확인할 강의 오브젝트
# OUTPUT: 가득 찼거나, 만료되었는지 여부
def is_closed(lect: Lect):
    flag = False
    # 강의가 가득 찼는가?
    if lect.lect_limit_num <= lect.get_enrolled_std_num:
        flag = True
    # 강의 모집 기간이 만료되었는가?
    if lect.is_expired:
        flag = True
    return flag


# 제작: 양태영
# 제작 내용: 일반회원 입장에서, 강의에 등록이 가능한지 확인하는 데코레이터
def enroll_check(func):
    @auth_check(active=True)
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        lect_no = -1
        if kwargs.get("lect_no"):
            lect_no = kwargs.get("lect_no")
        elif kwargs.get("room_no"):
            lect_no = kwargs.get("room_no")
        if lect_no != -1:
            lect = Lect.objects.get(pk=lect_no)
            if is_closed(lect):
                messages.warning(request, "강의가 마감되었습니다. 신청할 수 없습니다.")
                return redirect("lect_view", type_no=lect.lect_type.type_no)
        return func(request, *args, **kwargs)

    return wrapper


# 제작: 양테영
# 제작 내용: 일반회원 입장에서 강의에 입장이 가능한지 확인하는 데코레이터 enroll_check와는 다르게 강의실 입장 가능 여부를 판단함.
def room_enter_check(func):
    @auth_check(active=True)
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        lect_no = -1
        if kwargs.get("lect_no"):
            lect_no = kwargs.get("lect_no")
        elif kwargs.get("room_no"):
            lect_no = kwargs.get("room_no")
        if lect_no != -1:

            lect = Lect.objects.prefetch_related('enrolled_students').get(pk=lect_no)
            enrolled_students = lect.enrolled_students.all()
            current_user = get_logined_user(request)
            flag = False

            #### 처음 두개의 질문, 강의를 모집 마감 시킴. ####
            if lect.lect_limit_num <= lect.get_enrolled_std_num:  # 강의가 가득 찼는가?
                flag = True
            if lect.is_expired:  # 강의 모집 기간이 만료되었는가?
                flag = True

            #### 마지막 3개의 질문, 마감이나, 다른 조건이 있더라도 예외로 허용시킴. ####
            if len(enrolled_students.filter(student=get_logined_user(request))) != 0:  # 등록한 사람 중 자신이 있는가?
                flag = False
            if lect.lect_chief == current_user:  # 자신이 강의자인가?
                flag = False
            if role_check(current_user, 3, "lte"):  # 자신이 회장단인가?(1: 회장, 2: 부회장, 3: 운영팀 중 하나)
                flag = False

            #### flag에 따라 경고, 혹은 강의실로 입장하게 됨. ####
            if flag:
                messages.warning(request, "강의가 마감되었습니다.")
                return redirect("lect_view", type_no=lect.lect_type.type_no)
        return func(request, *args, **kwargs)

    return wrapper


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
            return not_allowed(request, error_404=True)

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
                return not_allowed(request)

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
                return not_allowed(request, error_404=True)

        return wrapper

    return decorator


# 데코레이터
# 제작일: 21.7.13
# 제작자: 유동현
# 수정일: 21.8.4
# 수정자: 양태영
# 용도: 강의 또는 스터디 구성원인지 확인하는 용도
# 수정 내용: 회장단도 해당 구성원에 포함.
def member_only(superuser=False):
    def decorator(func):
        @login_required
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            current_user = get_logined_user(request)

            try:
                lect_room = Lect.objects.prefetch_related(
                    'enrolled_students').get(pk=kwargs.get('room_no', kwargs.get('lect_no')))
            except Lect.DoesNotExist:
                messages.warning(request, "해당 강의를 찾을 수 없습니다. 삭제되었을 수 있습니다.")
                return redirect("lect_view", type_no=1)

            if current_user == lect_room.lect_chief:
                return func(request, *args, **kwargs)
            elif member := lect_room.enrolled_students.filter(student=current_user).first():
                if member.status_id == 1:
                    return func(request, *args, **kwargs)
            elif superuser and role_check(current_user, 3, "lte"):
                return func(request, *args, **kwargs)

            return not_allowed(request, msg='수강정지 되었거나, 접근할 수 없는 멤버입니다!')

        return wrapper

    return decorator


# 디폴트 프로필 사진의 경로를 얻어옴
def get_default_pic_path():
    return "member/default/default.png"


# 기존의 이미지 패스가 디폴트 패스인지 검사
def is_default_pic(img_path):
    return str(img_path) == get_default_pic_path()


# 제작: 양태영
# 제작 내용: 초기화를 할지 삭제를 할 지 결정하는 함수
# 제작 사유: 회원이 회원탈퇴를 결정하였을 때 중요한 게시판 (공지사항, 활동게시판, 공모전게시판, 예산, 연혁)에 관여한 경우
# 그냥 나가버리면 같이 관련된 부분이 삭제되어버림 그렇다고 null로 처리하게 되면 데이터 무결성을 해치게 되며, 책임소재를 묻기 어려우므로
# 해당 부분에 대해서 체크하는 함수.
# 관여가 되어있다면 delete_user에서 초기화시키는 과정을 밟게 됨.
def is_related(user: User):
    # 활동 게시판이랑 관련이 있는가?
    if len(Board.objects.filter(Q(board_writer=user) & Q(board_type_no__board_type_no=4))) != 0:
        return True
    # 공지 사항과 관련이 있는가?
    if len(Board.objects.filter(Q(board_writer=user) & Q(board_type_no__board_type_no=1))) != 0:
        return True
    # 공모전 게시판이랑 관련이 있는가?
    if len(ContestBoard.objects.filter(contest_writer=user)) != 0:
        return True
    # 예산 지원신청을 하였거나, 예산을 처리한 적이 있는가?
    if len(Bank.objects.filter(Q(bank_cfo=user) | Q(bank_used_user=user))) != 0:
        return True
    # 연혁에 개입하였는가?
    if len(History.objects.filter(history_writer=user)) != 0:
        return True
    # 정책에 개입하였는가?
    if len(PolicyTerms.objects.filter(policy_user=user)) != 0:
        return True
    return False


# 최소한의 개인정보(학번, 유저 이름)만 남기고 모든 정보를 초기화시키는 함수.
# IN: 초기화시킬 User 인스턴스
# OUT: 초기화시킨 User 인스턴스
def initialize_user(user: User):
    user.user_auth = None
    user.user_role = None
    user.user_phone = None
    user.user_major = None
    user.user_gen = None
    user.user_grade = None
    user.user_pic = get_default_pic_path()
    return user.save()


# 계정 초기화를 하면 모든 게시글이 사라지지 않으므로 자신과 연관된 모든 데이터를 지우는 함수.
def delete_all_infomation(user: User):
    # 본인 덧글 삭제
    my_comment_list = Comment.objects.filter(Q(comment_cont_ref__comment_writer=user))
    for my_comment in my_comment_list:
        my_comment.delete()
    my_comment_list = Comment.objects.filter(comment_writer=user)
    for my_comment in my_comment_list:
        my_comment.delete()
    # 본인 게시글 삭제(단 활동 게시판의 게시글은 공익을 위한 게시글이므로 삭제되어선 안된다.)
    my_board_list = Board.objects.filter(
        Q(board_writer=user) & ~Q(board_type_no__board_type_no=4) & ~Q(board_type_no__board_type_no=1))
    for my_board in my_board_list:
        FileController.delete_all_files_of_(my_board)
        comment_delete_by_post_delete(my_board)
        my_board.delete()

    # 본인이 제명 대상자로 있거나, 본인이 발안한 제명 안건 삭제
    my_user_delete_list = UserDelete.objects.filter(
        Q(suggest_user=user) | Q(deleted_user=user))
    for my_user_delete in my_user_delete_list:
        FileController.delete_all_files_of_(my_user_delete)
        comment_delete_by_post_delete(my_user_delete)
        my_user_delete.delete()

    # 본인이 작성한 강의실 게시글 삭제
    my_lect_board_list = LectBoard.objects.filter(lect_board_writer=user)
    for my_lect_board in my_lect_board_list:
        FileController.delete_all_files_of_(my_lect_board)
        comment_delete_by_post_delete(my_lect_board)
        my_lect_board.delete()

    # 본인이 수강중인 강의 삭제
    my_lect_enrollment_list = LectEnrollment.objects.filter(student=user)
    for my_lect_enrollment in my_lect_enrollment_list:
        my_lect_enrollment.delete()

    # 본인이 개설한 강의/스터디/취미모임 삭제
    my_lect_list = Lect.objects.filter(lect_chief=user)
    for my_lect in my_lect_list:
        FileController.delete_all_files_of_(my_lect)
        my_lect.delete()

    # 연동한 이메일 모두 삭제
    my_email_list = UserEmail.objects.filter(user_stu=user)
    for my_email in my_email_list:
        my_email.delete()

    # 가입 질문에 대한 답변 모두 삭제
    my_answer_list = Answer.objects.filter(answer_user=user)
    for my_answer in my_answer_list:
        my_answer.delete()
    # 본인 계정 프로필 사진 삭제
    if not is_default_pic(str(user.user_pic)):
        FileController.delete_all_files_of_(user)

    # 자신의 알람 삭제
    my_alarm_list = Alarm.objects.filter(alarm_user=user)
    for my_alarm in my_alarm_list:
        my_alarm.delete()

    # 자신의 출석 삭제
    my_lect_attendance_list = LectAttendance.objects.filter(student=user)
    for my_lect_attendance in my_lect_attendance_list:
        # 삭제는 되지만 DB.models -> LectAttendance -> student -> on_delete=SET_DEFAULT로 인해 DEFAULT_USER로 설정됨.
        my_lect_attendance.delete()


# 삭제 로직
def delete_user(user: User):
    if not user.user_role.role_no <= 4:
        with transaction.atomic():
            # 회계를 요청한 유저거나, 회계를 작성한 유저, 연혁을 작성한 유저, 활동 게시판 게시글을 작성한 유저,
            # 공모전 게시판의 게시글을 작성한 유저의 경우 데이터 무결성을 위해 최소한의 개인정보 만을 남기고 초기화시킴
            if is_related(user):
                initialize_user(user)  # 유저 정보 초기화
                delete_all_infomation(user)  # 유저의 게시글 및 흔적 모두 삭제
            # 회계나 연혁에 관련 없는 계정의 경우 DB에서 계정 완전 삭제

            else:
                if not is_default_pic(str(user.user_pic)):  # 프로필 사진인 디폴트 사진이 아닌 경우
                    FileController.delete_all_files_of_(user)  # 데이터 베이스에서 삭제함
                user.delete()
            return True
    return False
