from DB.models import User
# 로그인 시 세션을 저장하는 함수


# 로그인 세션을 등록하는 함수
def save_session(request, **kwargs):
    request.session["user_stu"] = kwargs.get("user_model").user_stu
    request.session["logined_email"] = kwargs.get("logined_email", '')
    request.session["provider"] = kwargs.get("provider", '')

