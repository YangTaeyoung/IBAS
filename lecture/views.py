from django.shortcuts import render

# Create your views here.
def contest_list(request):  # 게시판 페이지로 이동
    return render(request, 'contest_board.html', {})