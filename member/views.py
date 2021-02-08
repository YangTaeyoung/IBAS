from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.

from DB.models import AuthUser, User  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.


# Create your views here.

def join(request):
    user_token = request.POST.get("password")
    if request.POST.get("password") is not None:  # pass페이지에서 password가 파라미터로 넘어왔을 경우에
        tar_user = User.objects.filter(user_token=user_token)[0]
        if tar_user is None:
            user_id = AuthUser.objects.filter(password=user_token)[0]  # auth테이블에서 해당 패스워드가 있는지 조회.
            # 있다면 social account에서 앞서서 Auth의 primary key를 통해 가입한 친구의 pk를 넣어서 조회
            tar_member = SocialAccount.objects.filter(user_id=user_id.id)[0]  # quesyset의 첫번째 자료. 즉 로그인한 인원의 인스턴스 변수
            # extra_data: 사용자의 동의를 통해 얻어온 권한인 듯.
            email = tar_member.extra_data.get('email')  # 자동 완성을 위해 인스턴스 변수 설정
            name = tar_member.extra_data.get('name')  # 자동 완성을 위한 이름 설정
            context = {
                "email": email,
                "name": name,
                "token": request.POST.get("password")
            }
            return render(request, 'join.html', context)
        else:
            request.session["user"] = tar_user
            return render(request, "index.html", {})

    else:  # 파라미터가 제대로 넘어오지 않은 경우, 즉 비정상적인 경로를 통해 로그인 된 경우
        return redirect(request, 'index.html', {'lgn_is_failed': 1})  # 자바 스크립트 경고를 띄우기 위한 변수 지정 후 index로 보냄.


def join_chk(request):
    if request.method == "POST":
        user_auth = request.POST.get("user_auth")
        user_role = request.POST.get("user_role")
        user_email = request.POST.get("user_email")
        user_major = request.POST.get("user_major")
        user_name = request.POST.get("user_name")
        user_stu = request.POST.get("user_stu")
        user_grade = request.POST.get("user_grade")
        user_gen = request.POST.get("user_gen")
        user_token = request.POST.get("user_token")
        user = User.objects.create(
            user_name=user_name,
            user_stu=user_stu,
            user_email=user_email,
            user_grade=user_grade,
            user_auth=user_auth,
            user_gen=user_gen,
            user_major=user_major,
            user_role=user_role,
            user_token=user_token
        )
        user.save()
        tar_user = User.objects.filter(user_token=user_token)
        request.session["user"] = tar_user
        return render(request, "index.html", {})


def logout(request):
    request.session.clear()
    return render(request, "index.html", {})


def login(request):
    return render(request, 'login.html', {})
