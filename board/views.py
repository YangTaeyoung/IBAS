from django.shortcuts import render

def board(request):  # 입부신청 완료 페이지로 이동
    return render(request, 'board.html', {})
