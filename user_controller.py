from django.core.exceptions import ObjectDoesNotExist

from DB.models import User


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
