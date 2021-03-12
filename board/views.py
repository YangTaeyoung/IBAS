from django.shortcuts import render

def board(request):  # 게시판 페이지로 이동
    return render(request, 'board.html', {})

def detail(request):
    return render(request, 'detail.html', {})