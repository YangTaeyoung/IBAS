from django.shortcuts import render
from serializer import CommentSerializer
from user_controller import get_logined_user, auth_check,writer_only
from django.shortcuts import get_object_or_404
from DB.models import CommentType
from comment_controller import CommentSerializer
# Create your views here.

@auth_check()
def comment_register(request, type_no, board_ref):
    comment_type = get_object_or_404(CommentType, pk=type_no)


    if request.method == "POST":
        comment_form = CommentSerializer(request.POST)
        if comment_form.is_valid():
            comment_form.save(comment_type=comment_type,comment_board_ref=board_ref)
        pass

@auth_check()
def comment_ref_register(request, comment_id):
    if request.method == "POST":
        comment_form = CommentSerializer(instance=request.data)
        if comment_form.is_valid():
            pass

@writer_only(superuser=True)
def comment_delete(request):
    pass


def comment_update(request):
    pass


def comment_view(request):
    pass