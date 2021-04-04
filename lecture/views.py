from django.shortcuts import render

# Create your views here.
def contest_list(request):  # 게시판 페이지로 이동
    return render(request, 'contest_board.html', {})

def contest_register(request):  # 게시판 페이지로 이동
    return render(request, 'contest_register.html', {})

def contest_detail(request):  # 게시판 페이지로 이동
    return render(request, 'contest_detail.html', {})