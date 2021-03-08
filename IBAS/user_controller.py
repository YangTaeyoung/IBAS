from DB.models import User


def is_chief_exist():  # 회장 정보가 있는지 체크
    return len(User.objects.filter(user_role=1)) != 0


def is_sub_chief_exist():  # 부회장 정보가 있는지 체크
    return len(User.objects.filter(user_role=2)) != 0


def get_chief():  # 회장 정보를 가져옴
    if is_chief_exist():
        return User.objects.filter(user_role=1)[0]
    else:
        return None


def get_sub_chief():  # 부회장 정보를 가져옴
    if is_sub_chief_exist():
        return User.objects.filter(user_role=2)[0]
    else:
        return None


def get_logined_user(request):  # 로그인한 유저의 정보를 가져옴
    if request.session.get('user_stu') is not None:
        return User.objects.get(pk=request.session.get('user_stu'))
    else:
        return None
