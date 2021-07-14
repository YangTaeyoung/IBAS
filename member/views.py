from django.shortcuts import render, redirect, get_object_or_404
from allauth.socialaccount.models import SocialAccount, \
    SocialToken  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from django.urls import reverse
from DB.models import User, UserAuth, UserRole, QuestForm, Answer, UserEmail, \
    MajorInfo  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from django.http import HttpResponseRedirect
# 내가 만든 세션 모듈 불러오기
from . import session
from urllib.request import urlretrieve  # 인터넷에 있는 파일 다운로드
import os
from django.conf import settings
from user_controller import get_social_login_info
from django.db import transaction


# Create your views here.

def choose_std_or_pro(request):  # 학생인지, 교수인지 고르게 하는 것.
    if request.method == "POST":  # POST로 온 요청의 경우, 즉 정상적인 요청인 경우
        if request.POST.get("password") is not None:  # pass페이지에서 password가 파라미터로 넘어왔을 경우, 즉 정상적으로 구글 로그인을 마친 경우
            user_token = request.POST.get("password")  # 토큰 정보를 받음
            social_dict = get_social_login_info(user_token)
            # ------------------------------소셜 로그인으로 받은 정보 처리 끝---------------------------------------#
            if len(UserEmail.objects.filter(user_email=social_dict.get(
                    "email"))) == 0:  # 토큰 정보로 USER DB를 검색 했을 때 나오는 유저 정보가 없을 경우, 즉 입부 신청하지 않은 유저의 경우
                # 컨텍스트에 자동완성 정보를 등록
                stu_list = list()
                for user in User.objects.all():
                    stu_list.append(user.user_stu)

                # if len(User.objects.filter(
                #         user_email=email)) == 0:
                #     # 컨텍스트에 자동완성 정보를 등록
                #     stu_list = list()
                #     for user in User.objects.all():
                #         stu_list.append(user.user_stu)

                context = social_dict

                return render(request, 'std_or_pro.html', context)
            else:  # 이미 입부신청 되어있는 유저의 경우
                # tar_member에 유저 정보를 저장
                user_email = UserEmail.objects.get(pk=social_dict.get("email"))
                tar_member = user_email.user_stu
                # 로그인 및 정보 출력에 필요한 정보를 세션에 저장
                session.save_session(request, user_model=tar_member, logined_email=user_email.user_email,
                                     provider=social_dict.get("provider"))
                return redirect(reverse('index'))
    else:  # 파라미터가 제대로 넘어오지 않은 경우, 즉 비정상적인 경로를 통해 로그인 된 경우
        return render(request, "index.html", {'lgn_is_failed': 1})  # 자바 스크립트 경고를 띄우기 위한 변수 지정 후 index로 보냄.


def join(request):  # 회원 가입 페이지를 랜더링 하는 함수
    stu_list = list()  # 학생번호 리스트를 담을 변수.
    phone_list = list()  # 핸드폰 번호를 담을 변수.
    for user in User.objects.all():
        stu_list.append(user.user_stu)  # 학생 리스트에서 학번만 뽑아서 학번 리스트 생성
        phone_list.append(user.user_phone)

    context = {  # hidden을 통해서 받은 회원들의 정보를 받아서 붙여넣음.
        "email": request.POST.get("email"),  # 이메일
        "name": request.POST.get("name"),  # 이름
        "pic": request.POST.get("pic"),  # 프로필 사진
        "provider": request.POST.get("provider"),
        "user_role": request.POST.get("user_role"),  # 회원 역할 (학생 or 교수)
        "stu_list": stu_list,  # 학번 리스트
        "phone_list": phone_list,
        "quest_list": QuestForm.objects.all(),  # 질문 양식
        "major_list": MajorInfo.objects.all()  # 전공 리스트(전공 검색을 위해)
    }
    return render(request, "join.html", context)


def join_chk(request):  # 회원 가입 페이지로 부터 정보를 받
    if request.method == "POST":  # POST로 데이터가 들어왔을 경우, 안들어 왔다면 -> 비정상 적인 접근임. 일반적으로 GET을 통해서는 접근이 불가능 해야함.
        # 사용자 정보를 받아옴

        context = {  # 회원 가입 정보를 받아서 질문 폼으로 전송
            "user_auth": request.POST.get("user_auth"),
            "user_role": request.POST.get("user_role"),
            "user_email": request.POST.get("user_email"),
            "user_major": request.POST.get("user_major"),
            "user_name": request.POST.get("user_name"),
            "user_stu": request.POST.get("user_stu"),
            "user_grade": request.POST.get("user_grade"),
            "user_gen": request.POST.get("user_gen"),
            "user_phone": request.POST.get("user_phone"),
            "user_pic": request.POST.get("user_pic"),
            "provider": request.POST.get("provider"),
            "quest_list": QuestForm.objects.all()
        }
        # 질문/답변 폼으로 보냄
        return render(request, "quest.html", context)

    return render(request, "index.html", {'lgn_is_failed': 1})


def quest_chk(request):
    if request.method == "POST":  # POST로 데이터가 들어왔을 경우, 안들어 왔다면 -> 비정상 적인 접근임. 일반적으로 GET을 통해서는 접근이 불가능 해야함.
        # 사용자 정보를 받아옴
        user_auth = request.POST.get("user_auth")
        user_role = request.POST.get("user_role")
        user_email = request.POST.get("user_email")
        user_major = MajorInfo.objects.filter(major_name=request.POST.get("user_major"))[0]
        user_name = request.POST.get("user_name")
        user_stu = request.POST.get("user_stu")
        user_grade = request.POST.get("user_grade")
        user_gen = request.POST.get("user_gen")
        user_phone = request.POST.get("user_phone")
        user_pic = request.POST.get("user_pic")
        provider = request.POST.get("provider")
        if user_pic is not None:
            try:  # 자신의 폴더가 남아 있을 경우의 예외처리
                os.mkdir(settings.MEDIA_ROOT + "/member/" + user_stu)
            except FileExistsError:
                pass
            try:  #
                urlretrieve(user_pic, "/home/ibas/Django/IBAS/media/member/" + user_stu + "/" + user_stu + ".jpg")
                user_pic = "member/" + user_stu + "/" + user_stu + ".jpg"
            except FileNotFoundError:
                user_pic = "member/default/default.png"
                pass
        # 받은 정보로 user 모델 인스턴스 변수 생성
        # 사용자 정보를 DB에 저장
        with transaction.atomic():
            user = User.objects.create(
                user_name=user_name,  # 이름
                user_stu=user_stu,  # 학번
                user_grade=user_grade,  # 학년
                user_auth=get_object_or_404(UserAuth, pk=user_auth),  # 권한 번호
                user_gen=user_gen,  # 기수
                user_major=user_major,  # 전공
                user_role=get_object_or_404(UserRole, pk=user_role),  # 역할 정보
                user_phone=user_phone,  # 핸드폰 번호
                user_pic=user_pic  # 프로필 사진
            )
            UserEmail.objects.create(
                user_email=user_email,
                provider=provider,
                user_stu=user
            )
            if user_role == "6":  # 오직 일반 학생으로 가입했을 때만
                # 모든 질문 리스트를 뽑아옴: 질문이 몇번까지 있는지 알아야 답변을 몇번까지 했는지 알기 때문
                quest_list = QuestForm.objects.all()
                # 질문에 대한 답변을 저장하는 곳
                for quest in quest_list:
                    Answer.objects.create(
                        answer_quest=quest,
                        answer_cont=request.POST.get("answer_" + str(quest.quest_no)),
                        answer_user=user,
                    )
            session.save_session(request, user_model=user, logined_email=user_email,
                                 provider=provider)  # 자동 로그인을 위해 세션 등록
        return redirect(reverse("welcome"))  # 정상 회원가입 완료시 회원 가입 완료 페이지로 이동.
    return render(request, "index.html", {'lgn_is_failed': 1})  # 비정상 적인 접근 시 로그인 실패 메시지 출력과 함께 메인페이지 이동.


def pass_param(request):  # 구글 로그인으로 부터 파라미터를 받아 넘기는 페이지, 사용자에겐 보이지 않음.
    return render(request, "pass_login_param.html", {})


def logout(request):  # 로그아웃
    request.session.clear()  # 세션 초기화
    return HttpResponseRedirect('/user/accounts/logout')  # 구글 세션 초기화 링크


def login(request):  # 로그인 페이지로 이동
    return render(request, 'login.html', {})


def welcome(request):  # 입부신청 완료 페이지로 이동
    return render(request, 'welcome.html', {})
