from django.shortcuts import render, redirect, reverse
from DB.models import LectType, Lect, LectDay, LectUser, StateInfo, MethodInfo
from django.db.models import Q
from pagination_handler import get_paginator_list, get_page_object
from user_controller import get_logined_user




# Create your views here.
def lect_register(request):  # 게시판 등록 페이지로 이동
    if request.method == "GET":
        context = {
            "lect_type": LectType.objects.get(pk=request.GET.get("lect_type")),
            "method_list": MethodInfo.objects.all()
        }
        return render(request, 'lecture_register.html', context)
    else:
        lect = Lect()
        lect.lect_type = LectType.objects.get(pk=request.POST.get("lect_type"))
        if request.POST.get("lect_type") == 1:  # 강의일 경우 승인 여부에 따라 개설 결정
            lect.lect_state = StateInfo.objects.get(pk=1)
        else:  # 스터디, 취미모임의 경우 자동 승인
            lect.lect_state = StateInfo.objects.get(pk=3)
        lect.lect_chief = get_logined_user(request)
        lect.lect_deadline = request.POST.get("lect_deadline")
        lect.lect_title = request.POST.get("lect_title")
        lect.lect_intro = request.POST.get("lect_intro")
        lect.lect_curri = request.POST.get("lect_curri")
        lect.lect_limit_num = request.POST.get("lect_limit_num")
        lect.lect_pic = request.FILES.get("lect_pic")
        lect.lect_method = MethodInfo.objects.get(pk=request.POST.get("lect_method"))
        lect.lect_place_or_link = request.POST.get("lect_place_or_link")
        lect.save()
        return redirect("lect_detail", lect_no=lect.lect_no)


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
