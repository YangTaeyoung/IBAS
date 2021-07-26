from django.shortcuts import render, redirect, get_object_or_404
from allauth.socialaccount.models import SocialAccount, \
    SocialToken  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from django.urls import reverse
from DB.models import User, UserAuth, UserRole, QuestForm, Answer, UserEmail, \
    MajorInfo, UserSchedule  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from django.http import HttpResponseRedirect
# 내가 만든 세션 모듈 불러오기
from . import session
from urllib.request import urlretrieve  # 인터넷에 있는 파일 다운로드
import os
from django.conf import settings
from user_controller import get_social_login_info
from django.db import transaction
from member.forms import UserForm, UserEmailForm


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
    if request.method == "POST":
        stu_list = list()  # 학생번호 리스트를 담을 변수.
        phone_list = list()  # 핸드폰 번호를 담을 변수.
        for user in User.objects.all():
            stu_list.append(user.user_stu)  # 학생 리스트에서 학번만 뽑아서 학번 리스트 생성
            phone_list.append(user.user_phone)
        user_email = request.POST.get("email")
        user_role = request.POST.get("user_role")
        user_form = UserForm(
            initial={
                "user_name": request.POST.get("name"),
                "user_role": user_role,
                "user_auth": 3,
                "user_gen": UserSchedule.objects.get(pk=1).generation
            }
        )
        user_email_form = UserEmailForm(
            initial={
                "user_email": user_email,
                "provider": request.POST.get("provider")
            }
        )

        context = {  # hidden을 통해서 받은 회원들의 정보를 받아서 붙여넣음.
            "user_email": user_email,  # 단순 출력용
            "user_role": user_role,  # 분기용
            "user_form": user_form,
            "user_email_form": user_email_form,
            "pic": request.POST.get("pic"),  # 프로필 사진
            "stu_list": stu_list,  # 학번 리스트
            "phone_list": phone_list,
            "quest_list": QuestForm.objects.all(),  # 질문 양식
            "major_list": MajorInfo.objects.all()  # 전공 리스트(전공 검색을 위해)
        }
        return render(request, "join.html", context)
    return redirect("index")


def join_chk(request):  # 회원 가입 페이지로 부터 정보를 받
    if request.method == "POST":  # POST로 데이터가 들어왔을 경우, 안들어 왔다면 -> 비정상 적인 접근임. 일반적으로 GET을 통해서는 접근이 불가능 해야함.
        context = {  # 회원 가입 정보를 받아서 질문 폼으로 전송
            "user_pic": request.POST.get("user_pic"),
            "quest_list": QuestForm.objects.all()
        }
        # 사용자 정보를
        user_form = UserForm(request.POST)
        user_email_form = UserEmailForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            print("설정된 전공", user.user_major)
            new_user_form = UserForm(instance=user)
            new_user_email_form = UserEmailForm(
                initial={
                    "user_stu": user_email_form.data.get("user_stu"),
                    "user_email": user_email_form.data.get("user_email"),
                    "provider": user_email_form.data.get("provider"),
                }
            )
            context.update(user_form=new_user_form, user_email_form=new_user_email_form)

        # 질문/답변 폼으로 보냄
        return render(request, "quest.html", context)

    return render(request, "index.html", {'lgn_is_failed': 1})


def quest_chk(request):
    if request.method == "POST":  # POST로 데이터가 들어왔을 경우, 안들어 왔다면 -> 비정상 적인 접근임. 일반적으로 GET을 통해서는 접근이 불가능 해야함.
        # 사용자 정보를 받아옴
        user_form = UserForm(request.POST)
        user_email_form = UserEmailForm(request.POST)
        pic_url = request.POST.get("user_pic")
        if user_form.is_valid():
            user = user_form.save(pic_url=pic_url)
            if user_email_form.is_valid():
                print("form 유효함")
                # 받은 정보로 user 모델 인스턴스 변수 생성
                # 사용자 정보를 DB에 저장
                user_email = user_email_form.save()
                if user.user_role.role_no == 6:  # 오직 일반 학생으로 가입했을 때만
                    # 모든 질문 리스트를 뽑아옴: 질문이 몇번까지 있는지 알아야 답변을 몇번까지 했는지 알기 때문
                    quest_list = QuestForm.objects.all()
                    # 질문에 대한 답변을 저장하는 곳
                    for quest in quest_list:
                        Answer.objects.create(
                            answer_quest=quest,
                            answer_cont=request.POST.get("answer_" + str(quest.quest_no)),
                            answer_user=user,
                        )
                session.save_session(request, user_model=user, logined_email=user_email.user_email,
                                     provider=user_email.provider)  # 자동 로그인을 위해 세션 등록

            return redirect(reverse("welcome"))  # 정상 회원가입 완료시 회원 가입 완료 페이지로 이동.
        print(user_form.errors)
        print(user_email_form.errors)
    return redirect(reverse("index"))  # 비정상 적인 접근 시 로그인 실패 메시지 출력과 함께 메인페이지 이동.


def pass_param(request):  # 구글 로그인으로 부터 파라미터를 받아 넘기는 페이지, 사용자에겐 보이지 않음.
    return render(request, "pass_login_param.html", {})


def logout(request):  # 로그아웃
    request.session.clear()  # 세션 초기화
    return HttpResponseRedirect('/user/accounts/logout')  # 구글 세션 초기화 링크


def login(request):  # 로그인 페이지로 이동
    return render(request, 'login.html', {})


def welcome(request):  # 입부신청 완료 페이지로 이동
    return render(request, 'welcome.html', {})
