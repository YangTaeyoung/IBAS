from DB.models import User
# 로그인 시 세션을 저장하는 함수


def save_session(request, user):
    request.session["user_stu"] = user.user_stu
    request.session["user_name"] = user.user_name
    request.session["user_email"] = user.user_email
    if user.user_pic is not None:
        request.session["user_pic"] = user.user_pic
    else:
        request.session["user_pic"] = "0"
    request.session["user_joined"] = str(user.user_joined)
    print("날짜 제대로 출력 되나? ", str(user.user_joined))
    request.session["user_major"] = user.user_major
    request.session["user_phote"] = user.user_phone
    request.session["user_gen"] = user.user_gen
    request.session["user_grade"] = user.user_grade
    print("왔음?")
    request.session["user_role"] = user.user_role.role_no
    request.session["user_auth"] = user.user_auth.auth_no
    print("왔음?2")
