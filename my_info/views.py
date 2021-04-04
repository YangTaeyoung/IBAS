from django.shortcuts import render, redirect, reverse
from DB.models import Board, User, Comment, Lect, LectBoard, BoardType, UserRole, Bank
from django.conf import settings
import os


# Create your views here.
def my_info(request):
    if request.session.get("user_stu") is not None:
        my_info = User.objects.get(pk=request.session.get("user_stu"))
        my_board_list = Board.objects.filter(board_writer=my_info).order_by("board_type_no__board_type_no").order_by("-board_created")
        my_comment_list = Comment.objects.filter(comment_writer=my_info).order_by(
            "comment_board_no__board_type_no").order_by("-comment_created")
        my_bank_list = Bank.objects.filter(bank_used_user=my_info).order_by("-bank_used")
        context = {
            "my_board_list": my_board_list,
            "my_comment_list": my_comment_list,
            "my_bank_list": my_bank_list,
            "my_info": my_info
        }
        return render(request, 'my_info.html', context)
    else:
        return redirect(reverse("index"))


def user_pic_change(request):  # 프로필 사진 변경
    if request.method == "POST":  # POST로 넘어온 정보의 경우
        if request.session.get("user_stu") == request.POST.get("user_stu"):  # 로그인 한 세션에 학번과, POST로 넘겨져온 학번 정보가 일치할 경우
            user = User.objects.get(pk=request.session.get("user_stu"))  # 유저 정보 획득가
            try:  # 파일이 없을 경우의 예외처리
                os.remove(
                    settings.MEDIA_ROOT + 'member/' + str(user.user_stu) + "/" + str(user.user_pic))  # 기존에 저장된 사진 파일 삭
                os.rmdir(settings.MEDIA_ROOT + 'member/' + str(user.user_stu))  # 기존에 사진을 담고 있던 폴더 삭
                # 파일이 안에 있는 삭제에서 폴더를 삭제할 경우 오류 만남.
            except FileNotFoundError:
                pass  # 파일이 없는 경우 그냥 통과시킨다.
            user.user_pic = request.FILES.getlist("user_pic")[0]  # 넘겨온 파일로 대체
            user.save()
    else:
        return redirect(reverse("index"))  # 파


def user_pic_delete(request):
    if request.method == "POST":
        if request.session.get("user_stu") == request.POST.get("user_stu"):  # 로그인 한 세션에 학번과, POST로 넘겨져온 학번 정보가 일치할 경우
            user = User.objects.get(pk=request.session.get("user_stu"))  # 유저 정보 획득
            try:  # 파일이 없을 경우의 예외처리
                # 프로필 사진 파일 삭제
                os.remove(settings.MEDIA_ROOT + 'member/' + str(user.user_stu) + "/" + str(user.user_pic))
                # 프로필 사진을 보관했던 디텍터리 삭제
                os.rmdir(settings.MEDIA_ROOT + 'member/' + str(user.user_stu))
                # 파일이 안에 있는 삭제에서 폴더를 삭제할 경우 오류 만남.
            except FileNotFoundError:
                pass  # 파일이 없는 경우 그냥 통과시킨다.
            user.user_pic = settings.STATIC_URL + "/default_profile.png"  # 디폴트 이미지로 세팅
            user.save()  # 저장
            #
            return redirect(reverse('my_info'))
        return redirect(reverse("index"))  # 비정상적인 요청의 경우
    else:
        return redirect(reverse("index"))  # 비정상적인 요청의 경우
