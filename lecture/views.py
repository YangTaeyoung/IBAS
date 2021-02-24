from django.shortcuts import render, redirect, reverse
from DB.models import Lect, LectBoard, LectCheck, LectType, User, MethodInfo, StateInfo


# Create your views here.
def lect_list(request):  # 유저가 보는 강의 리스트 페이지

    lect_type = request.POST.get("lect_type")
    lect_li = Lect.objects.all()
    if lect_type is not None:
        lect_li = Lect.objects.filter(lect_type=LectType.objects.get(pk=lect_type))

    context = {'lect_list': lect_li}
    return render(request, "lect_list.html", context)


def lect_register(request):
    if request.method == "POST":
        lect = Lect.objects.create(
            lect_chief=User.objects.get(pk=request.session.get("user_stu")),
            lect_deadline=request.POST.get("lect_deadline"),
            lect_pic=request.POST.get("lect_pic"),
            lect_intro=request.POST.get("lect_intro"),
            lect_title=request.POST.get("lect_title"),
            lect_method=MethodInfo.objects.get(pk=request.POST.get('lect_method')),
            lect_place_or_link=request.POST.get("lect_place_or_link"),
            lect_curri=request.POST.get("lect_curri"),
            lect_limit_num=request.POST.get("lect_limit_num"),
            lect_type=LectType.objects.get(pk=request.POST.get('lect_type')),
        )
        lect.save()
        return redirect(reverse("lect_list"))
    else:
        return render(request, "lect_register.html", {})


def lect_update(request):
    if request.method == 'GET':  # 단순 페이지 이동
        if request.GET.get("lect_no") is not None:  # 정상적으로 수정할 강의 번호가 들어왔을 경우
            lect = Lect.objects.get(pk=request.POST.get('lect_no'))
            context = {'lect': lect}
        else:
            render(request, "index.html", {'lgn_is_failed': 1})

    else:  # 수정 후 리스트로 이동


def lect_delete(request):
