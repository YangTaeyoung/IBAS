from django.shortcuts import render
from DB.models import LectType, Lect, LectDay,LectUser
from django.db.models import Q
from pagination_handler import get_paginator_list, get_page_object
from user_controller import get_logined_user


# Create your views here.
def lect_register(request):  # 게시판 등록 페이지로 이동
    return render(request, 'lecture_register.html', {})


def lect_detail(request, lect_no):  # 게시판 상세 페이지로 이동
    lect = Lect.objects.get(pk=lect_no)
    lect_day_list = LectDay.objects.filter(lect_no=lect_no)
    context = {
        'lect' : lect,
        'lect_day_list': lect_day_list,
        'lect_user_num': len(LectUser.objects.filter(lect_no=lect_no))
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
