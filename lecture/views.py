from django.shortcuts import render
from DB.models import LectType, Lect


# Create your views here.
def lect_register(request):  # 게시판 등록 페이지로 이동
    return render(request, 'lecture_register.html', {})


def lect_detail(request, lect_no):  # 게시판 상세 페이지로 이동
    return render(request, 'lecture_detail.html', {})


def lect_view(request, type_no):  # 게시판 페이지로 이동
    lect_type = LectType.objects.get(pk=type_no)
    lect_list = Lect.objects.filter(lect_type=lect_type)
    context = {
        "type": lect_type,
        "lecture": LectType.objects.get(pk=1),
        "lecture_len": len(Lect.objects.filter(lect_type__type_no=1)),
        "study": LectType.objects.get(pk=2),
        "study_len": len(Lect.objects.filter(lect_type__type_no=2)),
        "habit": LectType.objects.get(pk=3),
        "habit_len": len(Lect.objects.filter(lect_type__type_no=3)),
        "lect_list": lect_list
    }
    return render(request, 'lecture_list.html', context)
