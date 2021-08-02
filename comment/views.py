import json

from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from comment.serializer import CommentSerializer
from user_controller import get_logined_user, auth_check, writer_only
from django.shortcuts import get_object_or_404
from DB.models import CommentType, Comment
from django.db.models import Q, F
from django.http.response import JsonResponse, HttpResponse
from rest_framework.response import Response

# url 기준  www.inhabas.com/comment/ ??? / .... /
# ??? 부분으로 구분
type_no = {
    'board': 1,
    'contest': 2,
    'lect': 3,
    'staff': 4,
}


def comment_register(request, type, board_ref):
    comment_type = get_object_or_404(CommentType, pk=type_no[type])

    if request.method == "POST":
        comment = Comment.objects.create(
            comment_type=comment_type,
            comment_writer=get_logined_user(request),
            comment_cont=json.loads(request.body)['comment_cont'],
            comment_board_ref=int(board_ref)
        )

        comment_json = {
            'comment_id': comment.comment_id,
            'writer_name': comment.comment_writer.user_name,
            'writer_major': comment.comment_writer.user_major.major_name,
            'comment_writer': comment.comment_writer_id,
            'comment_cont': comment.comment_cont,
            'comment_created': comment.comment_created,
            'comment_cont_ref': comment.comment_cont_ref
        }

        return JsonResponse({'comment': comment_json}, safe=False)
        # comment_form = CommentSerializer(request.POST)
        # if comment_form.is_valid():
        #     comment_form.save(comment_type=comment_type, comment_board_ref=board_ref)
        # pass
    else:
        return JsonResponse(status=400, data={})


def comment_ref_register(request, comment_id):
    if request.method == "POST":
        comment_form = CommentSerializer(instance=request.data)
        if comment_form.is_valid():
            pass
    else:
        return JsonResponse(status=400, data={})


@writer_only(superuser=True)
def comment_delete(request, comment_id):
    if request.method == "DELETE":
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()

        return JsonResponse(data={}, status=204)
    else:
        return JsonResponse(status=400, data={})


def comment_update(request, comment_id):
    if request.method == "PUT":
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.comment_cont = json.loads(request.body)['comment_cont']
        comment.save()

        comment_json = {
            'comment_id': comment.comment_id,
            'writer_name': comment.comment_writer.user_name,
            'writer_major': comment.comment_writer.user_major.major_name,
            'comment_writer': comment.comment_writer_id,
            'comment_cont': comment.comment_cont,
            'comment_created': comment.comment_created,
            'comment_cont_ref': comment.comment_cont_ref
        }

        return JsonResponse({'comment': comment_json}, safe=False)
    else:
        return JsonResponse(status=400, data={})


@ensure_csrf_cookie
def comment_view(request, type, board_ref):
    comment_list = Comment.objects.filter(
        Q(comment_type_id=type_no[type]) & Q(comment_board_ref=board_ref) & Q(
            comment_cont_ref__isnull=True)).prefetch_related("comment_ref").order_by("-comment_created")
    comment_serializer = CommentSerializer(comment_list, many=True)
    return Response(comment_serializer.data)


@ensure_csrf_cookie
def axios_response(request, type, board_ref):
    comments = Comment.objects.prefetch_related("comment_ref")\
        .filter(comment_cont_ref__isnull=True, comment_board_ref=board_ref, comment_type_id=type_no[type]) \
        .order_by("comment_created") \
        .annotate(
        writer_name=F('comment_writer__user_name'),
        writer_major=F('comment_writer__user_major__major_name')) \

    comment_set_list = [
        list(
            comment.comment_ref
                .annotate(
                    writer_name=F('comment_writer__user_name'),
                    writer_major=F('comment_writer__user_major__major_name'))
                .values(
                    'comment_id', 'writer_name', 'writer_major', 'comment_writer',
                    'comment_cont', 'comment_created', 'comment_cont_ref')
        )
        for comment in comments]

    comments = comments.values('comment_id', 'writer_name', 'writer_major', 'comment_writer',
                               'comment_cont', 'comment_created', 'comment_cont_ref')

    cur_user = get_logined_user(request)
    logined_user = {
        'user_role': cur_user.user_role_id,
        'user_stu': cur_user.user_stu
    }

    return JsonResponse({
        'comment_list': list(comments),
        'comment_set_list': comment_set_list,
        'logined_user': logined_user}, safe=False)