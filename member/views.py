from django.shortcuts import render, redirect,get_object_or_404
from allauth.socialaccount.models import SocialAccount, \
    SocialToken  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from django.urls import reverse
from DB.models import AuthUser, User, UserAuth, UserRole #AccountEmailaddress  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from django.http import HttpResponseRedirect
# 내가 만든 세션 모듈 불러오기
from . import session


# Create your views here.

def join(request):  # 회원 가입 페이지로 이동 할 것인지, 이미 있는 회원인지 판단하는 함수
    if request.method == "POST":
        if request.POST.get("password") is not None:  # pass페이지에서 password가 파라미터로 넘어왔을 경우에
            user_token = request.POST.get("password")
            if len(User.objects.filter(
                    user_token=user_token)) == 0:  # 토큰 정보로 USER DB를 검색 했을 때 나오는 유저 정보가 없을 경우, 즉 입부 신청하지 않은 유저의 경

                auth_user = AuthUser.objects.filter(password=user_token)[0]  # auth테이블에서 해당 패스워드가 있는지 조회.

                # 있다면 social account에서 앞서서 Auth의 primary key를 통해 가입한 친구의 pk를 넣어서 조회
                tar_member = SocialAccount.objects.filter(user_id=auth_user.id)[0]  # quesyset의 첫번째 자료. 즉 로그인한 인원의 인스턴스 변수
                tar_token = SocialToken.objects.filter(account_id=tar_member.id)[0]

                # extra_data: 사용자의 동의를 통해 얻어온 권한인 듯.
                email = tar_member.extra_data.get('email')  # 자동 완성을 위해 인스턴스 변수 설정
                name = tar_member.extra_data.get('name')  # 자동 완성을 위한 이름 설정
                context = {
                    "email": email,
                    "name": name,
                    "token": request.POST.get("password")
                }

                # 소셜 로그인으로 부터 받은 정보는 저장하지 않기 위해 해당 정보 삭제
                tar_token.delete()
                tar_member.delete()
                auth_user.delete()



                return render(request, 'join.html', context)
            else:  # 이미 입부신청 되어있는 유저의 경우
                # tar_member에 유저 정보를 저장
                tar_member = User.objects.filter(user_token=user_token)[0]
                # 로그인 및 정보 출력에 필요한 정보를 세션에 저장
                session.save_session(request, tar_member.user_stu, tar_member.user_name, tar_member.user_email,
                                     tar_member.user_token, tar_member.user_pic)
                return redirect(reverse('index'))
    else:  # 파라미터가 제대로 넘어오지 않은 경우, 즉 비정상적인 경로를 통해 로그인 된 경우
        return render(request, "index.html", {'lgn_is_failed': 1})  # 자바 스크립트 경고를 띄우기 위한 변수 지정 후 index로 보냄.


def join_chk(request):  # 회원 가입 페이지로 부터 정보를 받아 가입 처리를 하는 메서드
    if request.method == "POST":  # POST로 데이터가 들어왔을 경우, 안들어 왔다면 -> 비정상 적인 접근임. 일반적으로 GET을 통해서는 접근이 불가능 해야함.
        # 사용자 정보를 받아옴
        user_auth = get_object_or_404(UserAuth, pk=request.POST.get("user_auth"))
        user_role = get_object_or_404(UserRole, pk=request.POST.get("user_role"))
        user_email = request.POST.get("user_email")
        user_major = request.POST.get("user_major")
        user_name = request.POST.get("user_name")
        user_stu = request.POST.get("user_stu")
        user_grade = request.POST.get("user_grade")
        user_gen = request.POST.get("user_gen")
        user_token = request.POST.get("user_token")
        user_phone = request.POST.get("user_phone")
        is_activated = request.POST.get("is_activated")
        # 사용자 정보를 토대로 모델 객체 생성
        user = User.objects.create(
            user_name=user_name,
            user_stu=user_stu,
            user_email=user_email,
            user_grade=user_grade,
            user_auth=user_auth,
            user_gen=user_gen,
            user_major=user_major,
            user_role=user_role,
            user_token=user_token,
            user_phone=user_phone,
            is_activated=is_activated
        )

        # 사용자 정보를 DB에 저장
        user.save()
        # 등록한 사용자 정보를 호출
        tar_member = User.objects.filter(user_token=user_token)[0]
        # 해당 정보를 로그인 및 정보 출력에 필요한 정보를 세션에 저장
        session.save_session(request, tar_member.user_stu, tar_member.user_name, tar_member.user_email,
                             tar_member.user_token, tar_member.user_pic)
        # 메인 페이지로 이동 lgn_is_failed: 0 -> 로그인 성공 1 -> 로그인 실패
        return render(request, "index.html", {'lgn_is_failed': 0})
    return render(request, "index.html", {'lgn_is_failed': 1})


def pass_param(request):  # 구글 로그인으로 부터 파라미터를 받아 넘기는 페이지, 사용자에겐 보이지 않음.
    return render(request, "pass_login_param.html", {})


def logout(request):  # 로그아웃
    request.session.clear()  # 세션 초기화
    return HttpResponseRedirect('/')  # 메인 페이지로 이동


def login(request):  # 로그인 페이지로 이동
    return render(request, 'login.html', {})
