# 로그인 시 세션을 저장하는 함수
def save_session(request, user_stu, user_name, user_email, user_token, user_pic=None):
    request.session["user_stu"] = user_stu
    request.session["user_name"] = user_name
    request.session["user_email"] = user_email
    request.session["user_token"] = user_token
    request.session["user_pic"] = user_pic
