from DB.models import User

# 로그인 했는지 여부를 반환하는 함수
def is_logined(request):
    return request.session.get("user_stu") is not None

# 유저 관련 객체를 반환하는 컨트롤러

def get_logined_user(request):  # 로그인한 유저 객체 반환
    return User.objects.get(pk=request.session.get("user_stu"))


def get_user(user_stu):  # 학번을 넣어서 조회할 경우
    return User.objects.get(pk=user_stu)


def get_user_post(request):  # post를 사용해서 일반적으로 받아온 경우
    return User.objects.get(pk=request.POST.get("user_stu"))


def get_user_get(request):  # get를 사용해서 일반적으로 받아온 경우
    return User.objects.get(pk=request.GET.get("user_stu"))


