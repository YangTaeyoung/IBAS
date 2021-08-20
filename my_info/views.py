import json
import os

from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from DB.models import Board, User, Comment, Bank, UserUpdateRequest, UserEmail, StateInfo, MajorInfo, Lect, \
    LectEnrollment, BoardType
from django.db.models import Q

from alarm.alarm_controller import create_user_activate_alarm
from user_controller import get_logined_user, login_required, get_social_login_info, get_default_pic_path, \
    is_default_pic, delete_user
from django.conf import settings
from django.contrib import messages
from member.session import save_session
import hashlib


def get_ecrypt_value(value: str):
    return hashlib.md5(value.encode()).hexdigest()


# Create your views here.
@login_required
def my_info(request):  # 내 정보 출력
    my_comment_list = Comment.objects.filter(
        Q(comment_writer=get_logined_user(request)) & Q(comment_type_id=1)).order_by("-comment_created")
    for my_comment in my_comment_list:
        my_comment.board_type = Board.objects.get(pk=my_comment.comment_board_ref).board_type_no.board_type_name
    context = {
        "my_lect_ing_list": LectEnrollment.objects.filter(
            Q(student=get_logined_user(request)) & Q(lect_no__lect_state__state_no=3) & Q(status_id=1)),
        "my_lect_fin_list": LectEnrollment.objects.filter(
            Q(student=get_logined_user(request)) & Q(lect_no__lect_state__state_no=4) & Q(status_id=1)),
        "my_lect_made_list": Lect.objects.filter(Q(lect_chief=get_logined_user(request))),
        "my_board_list": Board.objects.filter(board_writer=get_logined_user(request)).order_by(
            "board_type_no").order_by("-board_created"),
        "my_comment_list": my_comment_list,
        "my_wait_request": UserUpdateRequest.objects.filter(
            Q(updated_user=get_logined_user(request)) & Q(updated_state__state_no=1)),
        "my_update_request_list": UserUpdateRequest.objects.filter(updated_user=get_logined_user(request)),
        "my_bank_list": Bank.objects.filter(bank_used_user=get_logined_user(request)).order_by("-bank_used"),
        "user_list": User.objects.all(),
        "major_list": MajorInfo.objects.all(),
        "is_naver_existed": len(
            UserEmail.objects.filter(Q(user_stu=get_logined_user(request)) & Q(provider="naver"))) != 0,
        "is_google_existed": len(
            UserEmail.objects.filter(Q(user_stu=get_logined_user(request)) & Q(provider="google"))) != 0,
    }
    return render(request, 'my_info.html', context)


def user_update_request_register(request):  # 이름 변경 신청
    if request.method == "POST":  # 포스트로 들어온 요청의 경우
        user_update_request = UserUpdateRequest.objects.create(  # 업데이트 신청 객체 생성
            updated_user_name=request.POST.get("updated_user_name"),
            updated_user=get_logined_user(request)  # 신청자: 로그인한 유저
        )
        user_update_request.save()  # 저장
    return redirect(reverse("my_info"))


# 유저 정보 수정 승인 거절 시 호출되는 함수.
def user_update_request_aor(request):
    if request.method == "POST":  # 포스트인가.
        updated_state = request.POST.get("updated_state")
        user_update_request = UserUpdateRequest.objects.get(pk=request.POST.get("updated_no"))

        # 승인 거절의 경우
        if updated_state == 2:
            user_update_request.updated_reject_reason = request.POST.get("updated_reject_reason")

        # 승인할 경우
        else:
            # 유저 이름 수정 반영
            user = user_update_request.updated_user
            user.user_name = user_update_request.updated_user_name
            user.save()

        user_update_request.updated_state = StateInfo.objects.get(pk=updated_state)  # 상태 업로드
        user_update_request.save()

    return redirect(reverse("my_info"))


def user_pic_update(request):
    if request.method == "POST":
        user_pic = request.FILES.get("user_pic")
        user = get_logined_user(request)
        if user_pic is not None:
            if not is_default_pic(user.user_pic):  # 만약 사용자의 이미지가 디폴트 이미지가 아니라면
                try:
                    os.remove(settings.MEDIA_ROOT + "/" + str(user.user_pic))  # 프  로필 이미지 삭제
                except FileNotFoundError:
                    pass
            # 새로운 이미지로 교체.
            user.user_pic = user_pic
            user.save()
    return redirect(reverse("my_info"))


@login_required
def user_pic_delete(request):
    user = get_logined_user(request)
    if not is_default_pic(user.user_pic):  # 기존에 있던 사진이 디폴트 사진이 아닌 경우.
        try:
            os.remove(settings.MEDIA_ROOT + "/" + str(user.user_pic))  # 이전 파일 삭제
        except FileNotFoundError:
            pass
    user.user_pic = get_default_pic_path()
    user.save()
    return redirect(reverse("my_info"))


@login_required
def user_major_update(request):
    current_user = get_logined_user(request)
    if len(MajorInfo.objects.filter(major_name=request.POST.get("user_major"))) != 0:
        current_user.user_major = MajorInfo.objects.filter(major_name=request.POST.get("user_major")).first()
        current_user.save()
    return redirect(reverse("my_info"))


@login_required
def user_phone_update(request):
    if request.method == "POST":
        current_user = get_logined_user(request)
        current_user.user_phone = request.POST.get("user_phone")
        current_user.save()
        return redirect(reverse("my_info"))

    elif request.method == "GET":
        user_phone = request.GET.get("user_phone", "")
        if len(User.objects.filter(user_phone=user_phone)):
            return JsonResponse(status=400, data={'msg': '중복되는 번호입니다.'})
        else:
            return JsonResponse(status=200, data={})

    else:
        return redirect(reverse("index"))


# 연동시 파라미터를 남기기 위한 코드 (GET 방식이기 때문에 보안에 매우 취약함.)
def go_social_login_before_setting(request):
    if request.method == "POST":
        encoded_user_stu = get_ecrypt_value(str(get_logined_user(request).user_stu))
        context = {
            "provider": request.POST.get("provider"),
            "next_url": "/user/pass?user_stu=" + encoded_user_stu,
        }
        return render(request, "go_social_login.html", context)
    return redirect(reverse("index"))


# login_required를 설정하지 말 것. 연동시 로그인이 잠시 풀리기 때문.
def connect_social_account(request):
    if request.method == "POST":
        social_dict = get_social_login_info(request.POST.get("password"))
        target_user_stu = request.POST.get("user_stu")
        current_user = None
        for user in User.objects.all():
            if target_user_stu == get_ecrypt_value(str(user.user_stu)):
                current_user = user
                break

        if current_user is not None:
            if len(UserEmail.objects.filter(user_email=social_dict.get("email"))) == 0:
                UserEmail.objects.create(user_stu=current_user, user_email=social_dict.get("email"),
                                         provider=social_dict.get("provider"))
                save_session(request, user_model=current_user, logined_email=social_dict.get("email"),
                             provider=social_dict.get("provider"))
                messages.warning(request, "정상적으로 이메일 연동이 완료되었습니다.")
                return redirect(reverse("my_info"))
            else:
                messages.warning(request, "이미 해당 이메일로 등록되어 있습니다.")
    else:
        messages.warning(request, "비 정상적인 접근입니다.")
    return redirect(reverse("index"))


# 회원 탈퇴 시 실행되는 함수,.
@login_required
def withdrawal(request):
    if request.method == "POST":
        if bool(request.POST.get("agreement")):
            if User.objects.get(pk=request.POST.get("user_stu")) == get_logined_user(request):
                current_user = get_logined_user(request)
                if delete_user(current_user):
                    return redirect("logout")  # 최후의 로그아웃 (세션 제거용)
    # 비정상적인 접근이거나(해킹 시도), 모종의 이유로 삭제되지 않은 경우
    return redirect(reverse("my_info"))  # 내 정보 페이지로 이동.


@login_required
def user_intro_update(request):
    if request.method == "POST":
        current_user = get_logined_user(request)
        if request.POST.get("user_apply_publish"):
            current_user.user_apply_publish = int(request.POST.get("user_apply_publish"))
        else:
            current_user.user_apply_publish = 0
        current_user.user_intro = request.POST.get("user_intro")
        current_user.save()
    return redirect(reverse('my_info'))


@login_required
def user_grade_update(request):
    if request.method == "POST":
        current_user = get_logined_user(request)
        current_user.user_grade = int(request.POST.get("user_grade"))
        current_user.save()
    return redirect(reverse('my_info'))


@login_required
def user_activate_request(request):
    current_user = get_logined_user(request)
    if current_user.user_auth.auth_no > 1:
        create_user_activate_alarm(current_user)
        messages.warning(request, "회비 납부 확인 요청이 완료되었습니다. \n\n순차적으로 확인하고 있으니 더 이상 요청하지 말아주세요.")
    return redirect("my_info")
