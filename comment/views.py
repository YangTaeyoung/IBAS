import json
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import ensure_csrf_cookie
from comment.serializer import CommentSerializer
from user_controller import get_logined_user, auth_check, writer_only, login_required
from django.shortcuts import get_object_or_404
from DB.models import CommentType, Comment, Board, User
from django.db.models import Q, F
from django.http.response import JsonResponse
from alarm.alarm_controller import create_comment_alarm

# url 기준  www.inhabas.com/comment/ ??? / .... /
# ??? 부분으로 구분
type_no = {
    'board': 1,
    'activity': 1,
    'contest': 2,
    'lect': 3,
    'staff': 4,
}


@auth_check()
def comment_register(request, type, board_ref):
    comment_type = get_object_or_404(CommentType, pk=type_no[type])

    if request.method == "POST":
        data = json.loads(request.body)
        comment = Comment(
            comment_type=comment_type,
            comment_writer=get_logined_user(request),
            comment_cont=data['comment_cont'].strip(),
            comment_board_ref=int(board_ref),
            comment_cont_ref_id=data.get('comment_cont_ref', None)
        )

        content = comment.comment_cont
        if not 0 < len(content) < 5001:
            raise ValidationError(
                code=400,
                message='댓글 내용 길이 제한을 확인하세요'
            )
        else:
            comment.save()
            create_comment_alarm(comment)
            serializer = CommentSerializer(comment)
            return JsonResponse({'comment': serializer.data}, safe=False)

    return JsonResponse(data={}, status=400)


@writer_only(superuser=True)
def comment_delete(request, comment_id):
    if request.method == "DELETE":
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()

        return JsonResponse(data={}, status=204)
    else:
        return JsonResponse(data={}, status=400)


@writer_only()
def comment_update(request, comment_id):
    if request.method == "PUT":
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.comment_cont = json.loads(request.body)['comment_cont']
        comment.save()

        serializer = CommentSerializer(comment)

        return JsonResponse({'comment': serializer.data}, safe=False)
    else:
        return JsonResponse(data={}, status=400)


@ensure_csrf_cookie
def comment_view(request, type, board_ref):
    if cur_user := User.objects.filter(pk=request.session.get("user_stu")).first():
        comment_list = Comment.objects.filter(
            Q(comment_type_id=type_no[type]) & Q(comment_board_ref=board_ref) & Q(
                comment_cont_ref__isnull=True)).prefetch_related("re_comments").order_by("comment_created")
        commentset_serializer = [CommentSerializer(comment.re_comments.all(), many=True).data for comment in comment_list]
        comment_serializer = CommentSerializer(comment_list, many=True)
        logined_user = {
            'user_role': cur_user.user_role_id,
            'user_stu': cur_user.user_stu
        }

        return JsonResponse({
            'comment_list': comment_serializer.data,
            'comment_set_list': commentset_serializer,
            'logined_user': logined_user}, safe=False, status=200)

    else:
        return JsonResponse({}, status=400)
