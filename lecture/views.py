from django.shortcuts import render, redirect, reverse
from DB.models import LectType, Lect, LectDay, LectUser, StateInfo, MethodInfo
from django.db.models import Q
from pagination_handler import get_paginator_list, get_page_object
from lecture.forms import LectForm, LectRejectForm, LectPicForm
from user_controller import get_logined_user, login_required, superuser_only, writer_only, auth_check
from file_controller import FileController
from django.utils.dateformat import DateFormat


def get_pol_name(method_no):
    pol_name = MethodInfo.objects.get(pk=method_no).method_name
    if method_no == 1:
        pol_name = "장소"
    elif method_no == 2:
        pol_name = pol_name + " 개인 링크"
    else:
        pol_name = pol_name + " 개인 채널 링크"
    return pol_name


# Create your views here.
@auth_check(active=True)
def lect_register(request):  # 강의/스터디/취미모임 등록 페이지로 이동하는 것
    if request.method == "GET":
        lect_type = LectType.objects.get(pk=request.GET.get("lect_type"))
        init_dict = {"lect_type": lect_type.type_no}
        if lect_type.type_no == 1:  # 강의일 때
            init_dict.update(lect_state=1)
        else:  # 강의가 아닐 때
            init_dict.update(lect_state=3)
        context = {
            "lect_type": lect_type,
            "method_list": MethodInfo.objects.all(),
            "lect_form": LectForm(initial=init_dict),
            "lect_pic_form": LectPicForm(),
            "is_update": False,
            "pol_name": get_pol_name(1)
        }
        return render(request, 'lecture_register.html', context)
    else:  # 강의/스터디/취미 모임 폼을 입력하고 전송 버튼을 눌렀을 경우
        lect_form = LectForm(request.POST)
        lect_pic_form = LectPicForm(request.POST, request.FILES)

        if lect_form.is_valid() and lect_pic_form.is_valid():
            lect = lect_form.save(lect_chief=get_logined_user(request))
            lect_pic_form.save(instance=lect)
            return redirect("lect_detail", lect_no=lect.lect_no)
        else:  # 유효성 검사 실패 시
            return redirect("lect_view", type_no=1)


@auth_check(active=True)
def lect_detail(request, lect_no):  # 게시판 상세 페이지로 이동
    lect = Lect.objects.get(pk=lect_no)
    lect_day_list = LectDay.objects.filter(lect_no=lect_no)
    context = {
        'lect': lect,
        'lect_day_list': lect_day_list,
        'lect_user_num': len(LectUser.objects.filter(lect_no=lect_no)),
        'is_in': len(LectUser.objects.filter(lect_user=get_logined_user(request))) >= 1,
        'lect_reject_form': LectRejectForm(instance=lect),
    }
    if lect.lect_method is not None:
        context.update(pol_name=get_pol_name(lect.lect_method.method_no))
    return render(request, 'lecture_detail.html', context)


@superuser_only
def lect_aor(request, lect_no):  # 강의 등록 거절 함수
    if request.method == "POST":
        lect_form = LectRejectForm(request.POST)
        if lect_form.is_valid():
            lect_form.update(instance=Lect.objects.get(pk=lect_no))
        return redirect("lect_detail", lect_no=lect_no)
    else:
        return redirect(reverse("index"))


@writer_only(superuser=False)
def lect_update(request, lect_no):
    lect = Lect.objects.get(pk=lect_no)
    lect.lect_deadline = DateFormat(lect.lect_deadline).format("Y-m-d")
    if request.method == "POST":
        lect_form = LectForm(request.POST)
        lect_pic_form = LectPicForm(request.POST, request.FILES)
        if lect_form.is_valid() and lect_pic_form.is_valid():
            lect_form.update(instance=lect)
            if lect_pic_form.has_changed():
                FileController.delete_all_files_of_(lect)
                lect_pic_form.save(instance=lect)
        return redirect("lect_detail", lect_no=lect.lect_no)
    else:  # 상세 페이지에서 수정 버튼을 눌렀을 때
        context = {
            "lect_type": lect.lect_type,
            "method_list": MethodInfo.objects.all(),
            "lect_form": LectForm(instance=lect),
            "lect_pic_form": LectPicForm(instance=lect),
            "is_update": True,
            "lect_no": lect.lect_no,
        }
        if lect.lect_method is not None:
            context.update(pol_name=get_pol_name(lect.lect_method.method_no))
        return render(request, "lecture_register.html", context)


@writer_only(superuser=True)
def lect_delete(request, lect_no):
    lect = Lect.objects.get(pk=lect_no)
    if request.method == "POST":
        lect_type_no = lect.lect_type.type_no
        FileController.delete_all_files_of_(lect)
        lect.delete()
        return redirect("lect_view", type_no=lect_type_no)
    return redirect("lect_detail", lect_no=lect.lect_no)


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
