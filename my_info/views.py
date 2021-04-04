from django.shortcuts import render,redirect,reverse
from DB.models import Board, User, Comment, Lect, LectBoard, BoardType, UserRole, Bank


# Create your views here.
def my_info(request):
    if request.session.get("user_stu") is not None:
        my_info = User.objects.get(pk=request.session.get("user_stu"))
        my_board_list = Board.objects.filter(board_writer=my_info).order_by("board_type_no").order_by("-board_created")
        my_comment_list = Comment.objects.filter(comment_writer=my_info).order_by("comment_board_no__board_type_no").order_by("-comment_created")
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
