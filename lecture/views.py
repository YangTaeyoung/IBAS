from django.shortcuts import render

# Create your views here.
def lect_list(request):  # 게시판 페이지로 이동
    return render(request, 'lecture_list.html', {})

