from django.shortcuts import render

# Create your views here.
def lecture_register(request):  # 게시판 등록 페이지로 이동
    return render(request, 'lecture_register.html', {})

def lecture_detail(request):  # 게시판 상세 페이지로 이동
    return render(request, 'lecture_detail.html', {})
def lect_list(request):  # 게시판 페이지로 이동
    return render(request, 'lecture_list.html', {})

