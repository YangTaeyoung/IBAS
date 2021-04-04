from django.shortcuts import render, get_object_or_404, reverse, redirect
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from DB.models import AuthUser, User, ChiefCarrier, UserRole, Board, BoardFile, \
    BoardType, Comment, History  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from django.db.models import QuerySet
from member import session
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.conf import settings
from IBAS.user_controller import is_chief_exist, is_sub_chief_exist, get_sub_chief, get_chief
import os
from IBAS.file_controller import get_filename, get_filename_with_ext

# Create your views here.

def staff_member_list(request):
    if request.session.get("user_role") <= 2: # 회원에 대한 관리는 회장과 부회장만 할 수 있음.
        member_list = User.objects.all() # 모든 유저 리스트를 가져 옴
        context = { # 컨텍스트에 등록
            "member_list" :member_list
        }
        return render(request, "member_manage.html", context) # 유저 리스트 페이지를 랜더링
    else: # 그 외의 권한을 가진 자가 접근할 경우 (해킹 시도)
        return redirect(reverse("index")) # 메인페이지로 보냄



def staff_member_update(request):
    if request.method == "POST": # 파라미터가 POST로 넘어왔는가? (정상적인 접근)
        user_stu_list = request.POST.getlist("user_stu_list[]")
        user_role = request.POST.get("user_role")
        user_auth = request.POST.get("user_auth")
        for user in User.objects.all(): # 모든 유저 순회
            for user_stu in user_stu_list: # 사용자가 권한을 바꾸기로 한 학번 리스트를 순회
                if user.user_stu == user_stu: # 만약 사용자가 선택한 학번의 친구와 기존에 유저의 학번이 일치할 경우. 즉, 사용자가 선택한 학번의 학생인 경우
                    if user_role is not None: # 바꾸려고 한 user_role가 있는 경우(사용자가 역할을 바꾸기로 결정한 경우)
                        user.user_role.role_no = user_role # 유저 역할 수정
                    if user_auth is not None: # 바꾸려고 한 user_auth가 있는 경우(사용자가 권한을 바꾸기로 결정한 경우)
                        user.user_auth.auth_no = user_auth # 유저 권한 수정
                    user.save() # DB 수정 내역 저장
        return redirect(reverse("staff_member_list"))
    else: # GET으로 넘어온 경우 비정상적인 접근.
        return redirect(reverse("index"))



def member_delete_list(request):
    context = {}
    return render(request, 'member_delete_list.html', context)

def member_delete_detail(request):
    context = {}
    return render(request, 'member_delete_detail.html', context)

def member_delete_register(request):
    context = {}
    return render(request, 'member_delete_register.html', context)