from DB.models import User
# 로그인 시 세션을 저장하는 함수


# 로그인 세션을 등록하는 함수
def save_session(request, user):
    request.session["user_stu"] = user.user_stu

