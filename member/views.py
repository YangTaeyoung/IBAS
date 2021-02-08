from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from pip._internal import req
from django.urls import reverse
from DB.models import AuthUser, User  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from django.http import HttpResponseRedirect

# Create your views here.

def join(request):
    user_token = request.POST.get("password")
    if request.POST.get("password") is not None:  # pass페이지에서 password가 파라미터로 넘어왔을 경우에
        if len(User.objects.filter(
                user_token=user_token)) == 0:  # 토큰 정보로 USER DB를 검색 했을 때 나오는 유저 정보가 없을 경우, 즉 입부 신청하지 않은 유저의 경

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
        else:  # 이미 입부신청 되어있는 유저의 경우
            print("길이", len(User.objects.filter(user_token=user_token)))
            # tar_member에 유저 정보를 저장
            tar_member = User.objects.filter(user_token=user_token)[0]
            # 로그인 및 정보 출력에 필요한 정보를 세션에 저장
            request.session["user_stu"] = tar_member.user_stu
            request.session["user_name"] = tar_member.user_name
            request.session["user_email"] = tar_member.user_email
            request.session["user_token"] = tar_member.user_token
            request.session["user_pic"] = tar_member.user_pic

            return redirect(reverse('index'))

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
        print("TEST: input -> var")
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
        print("TEST: create")
        user.save()
        print("TEST: save")
        tar_member = User.objects.filter(user_token=user_token)[0]
        request.session["user"] = tar_member
        return render(request, "index.html", {'lgn_is_failed': 0})
    return render(request, "index.html", {'lgn_is_failed': 1})


def pass_param(request):
    return render(request, "pass_login_param.html", {})


def logout(request):
    request.session.clear()
    return HttpResponseRedirect('/user/accounts/logout')


def login(request):
    return render(request, 'login.html', {})
