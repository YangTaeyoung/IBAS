import os

from django.shortcuts import render, redirect, reverse
from DB.models import Board, User, Comment, Lect, LectBoard, BoardType, UserRole, Bank, UserAuth, UserUpdateRequest, \
    StateInfo
from django.db.models import Q
from django.core.paginator import Paginator
from pagination_handler import get_paginator_list
from user_controller import get_logined_user, get_user
from django.conf import settings


# Create your views here.
def my_info(request):  # 내 정보 출력
    if request.session.get("user_stu") is not None:
        my_info = get_logined_user(request)
        my_board_list = Board.objects.filter(board_writer=my_info).order_by("board_type_no").order_by("-board_created")
        my_comment_list = Comment.objects.filter(comment_writer=my_info).order_by(
            "comment_board_no__board_type_no").order_by("-comment_created")
        my_bank_list = Bank.objects.filter(bank_used_user=my_info).order_by("-bank_used")
        my_wait_request = UserUpdateRequest.objects.filter(
            Q(updated_user=get_logined_user(request)) & Q(updated_state__state_no=1))
        my_update_request_list = UserUpdateRequest.objects.filter(updated_user=get_logined_user(request))
        new_user_list = User.objects.filter(user_auth__auth_no=3)  # 신입 부원 리스트
        exist_user_list = User.objects.filter(~Q(user_auth__auth_no=3))  # 기존 회원 리스트
        new_user_items = get_paginator_list(request, "new_user", new_user_list, 10)
        exist_user_items = get_paginator_list(request, "exist_user", exist_user_list, 2)
        auth_list = UserAuth.objects.filter(auth_no__lte=2)  # 기존 회원은 미승인 회원으로 넘길 수 없으므로, role_no 가 2 이하인 튜플만 가져옴.
        role_list = UserRole.objects.all()
        context = {
            "my_board_list": my_board_list,
            "my_comment_list": my_comment_list,
            "my_wait_request": my_wait_request,
            "my_update_request_list ": my_update_request_list,
            "my_bank_list": my_bank_list,
            "my_info": my_info,
            "exist_user_list": exist_user_items,
            "exist_user_len": len(exist_user_list),
            "new_user_list": new_user_items,
            "new_user_len": len(new_user_list),
            "auth_list": auth_list,
            "role_list": role_list
        }
        return render(request, 'my_info.html', context)
    else:
        return redirect(reverse("index"))


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
            if str(user.user_pic) != "member/default/default.png":  # 만약 사용자의 이미지가 디폴트 이미지가 아니라면
                try:
                    os.remove(settings.MEDIA_ROOT + "/" + str(user.user_pic))  # 프로필 이미지 삭제
                except FileNotFoundError:
                    pass
            # 새로운 이미지로 교체.
            user.user_pic = user_pic
            user.save()
            request.session["user_pic"] = str(user.user_pic)
    return redirect(reverse("my_info"))


def user_pic_delete(request):
    user = get_logined_user(request)
    if str(user.user_pic) != "member/default/default.png":  # 기존에 있던 사진이 디폴트 사진이 아닌 경우.
        try:
            os.remove(settings.MEDIA_ROOT + "/" + str(user.user_pic))  # 이전 파일 삭제
        except FileNotFoundError:
            pass
    user.user_pic = "member/default/default.png"
    return redirect(reverse("my_info"))
