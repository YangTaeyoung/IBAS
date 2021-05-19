from django.shortcuts import render, redirect, reverse
from DB.models import LectType, Lect, LectDay, LectUser, StateInfo, MethodInfo
from django.db.models import Q
from pagination_handler import get_paginator_list, get_page_object
from user_controller import get_logined_user
from lecture.forms import LectForm
from user_controller import login_required


# Create your views here.
@login_required
def lect_register(request):  # 강의/스터디/취미모임 등록 페이지로 이동하는 것
    if request.method == "GET":
        lect_type = LectType.objects.get(pk=request.GET.get("lect_type"))
        init_dict = {"lect_type": lect_type.type_no, "lect_reject_reason": None}
        if lect_type == 1:  # 강의일 때
            init_dict.update(lect_state=1)
        else:  # 강의가 아닐 때
            init_dict.update(lect_state=3)
        context = {
            "lect_type": lect_type,
            "method_list": MethodInfo.objects.all(),
            "lect_form": LectForm(initial=init_dict)
        }
        return render(request, 'lecture_register.html', context)
    else:  # 강의/스터디/취미 모임 폼을 입력하고 전송 버튼을 눌렀을 경우
        lect_form = LectForm(request.POST)
        if lect_form.is_valid():
            print("유효성 검사 성공")
            lect = lect_form.save()
            return redirect("lect_detail", lect_no=lect.lect_no)
        else:  # 유효성 검사 실패 시
            print("유효성 검사 실패")
            return redirect("lect_view", type_no=1)


def lect_detail(request, lect_no):  # 게시판 상세 페이지로 이동
    lect = Lect.objects.get(pk=lect_no)
    lect_day_list = LectDay.objects.filter(lect_no=lect_no)
    context = {
        'lect': lect,
        'lect_day_list': lect_day_list,
        'lect_user_num': len(LectUser.objects.filter(lect_no=lect_no)),
        'is_in': len(LectUser.objects.filter(lect_user=get_logined_user(request))) >= 1
    }
    return render(request, 'lecture_detail.html', context)


def lect_view(request, type_no):  # 게시판 페이지로 이동
    lect_type = LectType.objects.get(pk=type_no)

    # 회장단에 의해 승인된 강의만 등록, 스터디는 등록 시 이미 승인.
    lect_list = get_page_object(request, Lect.objects.filter(
        Q(lect_type=lect_type) & Q(lect_state__state_no=3)).prefetch_related(
        "lectday_set").prefetch_related("lectuser_set"))
    context = {
        "type": lect_type,
        "lecture": LectType.objects.get(pk=1),
        "lect_list": lect_list
    }
    return render(request, 'lecture_list.html', context)
