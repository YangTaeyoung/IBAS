from django.shortcuts import render, redirect, reverse
from DB.models import Board, User, Comment, Lect, LectBoard, BoardType, UserRole, Bank, UserAuth
from django.db.models import Q
from django.core.paginator import Paginator
from pagination_handler import get_paginator_list


# Create your views here.
def my_info(request):
    if request.session.get("user_stu") is not None:
        my_info = User.objects.get(pk=request.session.get("user_stu"))
        my_board_list = Board.objects.filter(board_writer=my_info).order_by("board_type_no").order_by("-board_created")
        my_comment_list = Comment.objects.filter(comment_writer=my_info).order_by(
            "comment_board_no__board_type_no").order_by("-comment_created")
        my_bank_list = Bank.objects.filter(bank_used_user=my_info).order_by("-bank_used")
        new_user_list = User.objects.filter(user_auth__auth_no=3)  # 신입 부원 리스트
        exist_user_list = User.objects.filter(~Q(user_auth__auth_no=3))  # 기존 회원 리스트
        new_user_items = get_paginator_list(request, "new_user", new_user_list, 10)
        exist_user_items = get_paginator_list(request, "exist_user", exist_user_list, 2)
        auth_list = UserAuth.objects.filter(auth_no__lte=2)  # 기존 회원은 미승인 회원으로 넘길 수 없으므로, role_no 가 2 이하인 튜플만 가져옴.
        role_list = UserRole.objects.all()
        context = {
            "my_board_list": my_board_list,
            "my_comment_list": my_comment_list,
            "my_bank_list": my_bank_list,
            "my_info": my_info,
            "exist_user_list": exist_user_items,
            "exist_user_len": len(exist_user_list),
            "new_user_list": new_user_items,
            "new_user_len":len(new_user_list),
            "auth_list": auth_list,
            "role_list": role_list
        }
        return render(request, 'my_info.html', context)
    else:
        return redirect(reverse("index"))
