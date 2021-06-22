from django.shortcuts import render, redirect, reverse
from DB.models import LectType, Lect, LectDay, LectUser, StateInfo, MethodInfo
from django.db.models import Q
from pagination_handler import get_paginator_list, get_page_object
from lecture.forms import LectForm, LectRejectForm, LectPicForm
from user_controller import get_logined_user, login_required, superuser_only, writer_only, auth_check, is_superuser, \
    is_logined
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

# 타입에 맞는 강의 리스트를 반환하는 함수
def get_lect_list(request, type_no):
    if type_no != 4:  # 강의 개설 신청 게시판이 아닌 일반 게시판(강의, 스터디, 취미모임)의 경우
        lect_type = LectType.objects.get(pk=type_no)
        lect_list = Lect.objects.filter(Q(lect_type=lect_type) & Q(lect_state__state_no=3)).prefetch_related(
            "lectday_set").prefetch_related("lectuser_set")
    else:
        lect_list = Lect.objects.filter(Q(lect_type=LectType.objects.get(pk=1)) & Q(lect_state__state_no=1) | Q(
            lect_state__state_no=2)).prefetch_related("lectday_set").prefetch_related("lectuser_set")
    return lect_list


# 타입에 맞는 강의 타입 인스턴스를 반환하는 함수
def get_lect_type(request, type_no):
    if type_no != 4:
        lect_type = LectType.objects.get(pk=type_no)
    else:
        if not is_logined(request) or not is_superuser(request):  # 강의 개설 관련 처리는 관리자만 할 수 있으므로 관리자 권한 체크
            return redirect(reverse("index"))
        lect_type = LectType()
        lect_type.type_no = type_no
        lect_type.type_no = 4
        lect_type.type_name = "강의 개설 신청"
        lect_type.type_exp = "개설 신청된 강의 목록입니다."
    return lect_type


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
        # 폼 유효성 검증
        if lect_form.is_valid() and lect_pic_form.is_valid():  # 유효성 검사 성공 시
            lect = lect_form.save(lect_chief=get_logined_user(request))
            lect_pic_form.save(instance=lect)
            return redirect("lect_detail", lect_no=lect.lect_no)
        else:  # 유효성 검사 실패 시
            return redirect("lect_view", type_no=1)


# 강의 상세 페이지로 이동 (활동 회원만 가능)
@auth_check(active=True)
def lect_detail(request, lect_no):
    lect = Lect.objects.get(pk=lect_no)
    lect_day_list = LectDay.objects.filter(lect_no=lect_no)
    context = {
        'lect': lect,
        'lect_day_list': lect_day_list,
        'lect_user_num': len(LectUser.objects.filter(lect_no=lect_no)),
        'is_in': len(LectUser.objects.filter(lect_user=get_logined_user(request))) >= 1,
        'lect_reject_form': LectRejectForm(instance=lect),
    }
    # 취미 모임의 경우 강의 방식이 없음 따라서 해당 부분에 대한 예외처리
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


# 강의를 수정하는 함수
@writer_only(superuser=False)
def lect_update(request, lect_no):
    lect = Lect.objects.get(pk=lect_no)
    lect.lect_deadline = DateFormat(lect.lect_deadline).format("Y-m-d")
    if request.method == "POST":  # 폼에 수정데이터를 입력 후 수정 버튼을 눌렀을 때
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


# 강의 삭제 함수
@writer_only(superuser=True)
def lect_delete(request, lect_no):
    lect = Lect.objects.get(pk=lect_no)
    if request.method == "POST":
        lect_type_no = lect.lect_type.type_no  # 강의 삭제 전 DB에 저장되어 있는 게시판 타입을 받아옴: 강의 리스트로 페이지를 리다이렉팅 하기 위함.
        FileController.delete_all_files_of_(lect)  # 강의에 저장되어 있는 사진 삭제
        lect.delete()  # 강의 DB에서 삭제
        return redirect("lect_view", type_no=lect_type_no)  # 강의 리스트로 페이지 전환
    return redirect("lect_detail", lect_no=lect.lect_no)


# 강의 리스트 이동 함수
def lect_view(request, type_no):  # 게시판 페이지로 이동
    lect_list = get_page_object(request, get_lect_list(request, type_no))
    lect_type = get_lect_type(request, type_no)
    context = {
        "type": lect_type,
        "item_list": lect_list
    }
    return render(request, 'lecture_list.html', context)  # 정상 처리


# 게시글 검색 시 이동 함수
def lect_search(request, type_no):
    keyword = request.GET.get("keyword")
    lect_type = get_lect_type(request,type_no)
    # 기존 리스트에 검색 필터 추가 (검색 범위: 강의 제목, 강의 계획, 강의 소개)
    lect_list = get_page_object(request, get_lect_list(request, type_no).filter(
        Q(lect_intro__icontains=keyword) | Q(lect_title__icontains=keyword) | Q(
            lect_chief__user_name__icontains=keyword)), num_of_boards_in_one_page=9)
    lect_type.type_exp = "\"" + keyword + "\"(으)로 검색한 결과입니다."
    context = {
        "type": lect_type,
        "item_list": lect_list
    }
    return render(request, 'lecture_list.html', context)  # 정상 처리

def lectRoom_main(request):  # 강의룸 페이지로 이동
    return render(request, 'lectRoom_main.html', {})