from django.shortcuts import render
from comment.serializer import CommentSerializer
from user_controller import get_logined_user, auth_check, writer_only
from django.shortcuts import get_object_or_404
from DB.models import CommentType, Comment
from django.db.models import Q, F
from django.http.response import JsonResponse,HttpResponse
from rest_framework.response import Response

# Create your views here.

@auth_check()
def comment_register(request, type_no, board_ref):
    comment_type = get_object_or_404(CommentType, pk=type_no)

    if request.method == "POST":
        comment_form = CommentSerializer(request.POST)
        if comment_form.is_valid():
            comment_form.save(comment_type=comment_type, comment_board_ref=board_ref)
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


def comment_view(request, type_no, board_ref):
    comment_list = Comment.objects.filter(
        Q(comment_type__comment_type_no=type_no) & Q(comment_board_ref=board_ref) & Q(
            comment_cont_ref__isnull=True)).prefetch_related("comment_ref").order_by("-comment_created")
    comment_serializer = CommentSerializer(comment_list, many=True)
    return Response(comment_serializer.data)


def axios_response(request):
    comments = Comment.objects.all() \
        .filter(comment_cont_ref__isnull=True) \
        .order_by("comment_created") \
        .annotate(
        writer_name=F('comment_writer__user_name'),
        writer_major=F('comment_writer__user_major__major_name')) \
        .prefetch_related("comment_set")

    comment_set_list = [
        list(
            comment.comment_set.all() \
                .annotate(
                    writer_name=F('comment_writer__user_name'),
                    writer_major=F('comment_writer__user_major__major_name')) \
                .values(
                    'comment_id', 'writer_name', 'writer_major', 'comment_writer',
                    'comment_cont', 'comment_created', 'comment_cont_ref')
        )
        for comment in comments]

    comments = comments.values('comment_id', 'writer_name', 'writer_major', 'comment_writer',
                               'comment_cont', 'comment_created', 'comment_cont_ref')

    return JsonResponse({'comment_list': list(comments), 'comment_set_list': comment_set_list}, safe=False)