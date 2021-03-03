from DB.models import User
# 로그인 시 세션을 저장하는 함수


# 로그인 세션을 등록하는 함수
def save_session(request, user):
    request.session["user_stu"] = user.user_stu
    request.session["user_name"] = user.user_name
    request.session["user_email"] = user.user_email
    if user.user_pic is not None: # 프로필 사진 있을 경우
        request.session["user_pic"] = str(user.user_pic)
    else: # 프로필 사진이 없을 경우
        request.session["user_pic"] = "0" # 0이 입력, 0일 경우 프로필 사진을 대체 이미지로 변경하면 될 듯.
    request.session["user_joined"] = str(user.user_joined)
    request.session["user_major"] = user.user_major.major_name
    request.session["user_phone"] = user.user_phone
    request.session["user_gen"] = user.user_gen
    request.session["user_grade"] = user.user_grade
    request.session["user_role"] = user.user_role.role_no
    request.session["user_auth"] = user.user_auth.auth_no
    request.session["is_activated"] = user.is_activated

# 회장(하단바)를 보여주기 위한 세션을 등록하는 함수
def save_chief(request, user):
    request.session["chief_name"] = user.user_name
    request.session["chief_phone"] = user.user_phone
    request.session["chief_email"] = user.user_email
