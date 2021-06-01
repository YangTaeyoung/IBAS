from django.core import serializers
import json
from django.db.models import F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from DB.models import Board, ContestBoard, LectBoard, Comment, ContestComment, LectBoardComment, User
from alarm.alarm_controller import create_comment_alarm, create_comment_ref_alarm
from user_controller import writer_only, auth_check


@auth_check()
def comment_register(request):
    pk = request.POST.get('pk')
    writer = request.session.get('user_stu')
    contents = request.POST.get('comment_cont')
    comment = None

    # 댓글
    if request.method == "POST":
        if Board:  # board 인지 구별하는 코드 생각하기!
            board = get_object_or_404(Board, pk=pk)  # 게시글 번호 들고오는 것임
            comment = Comment.objects.create(
                comment_board_no=board,  # 해당 게시글에
                comment_writer=writer,  # 해당 학번이
                comment_cont=contents  # 사용자가 쓴 내용을 가져옴
            )

        elif ContestBoard:  # contest 인지 구별하는 코드 생각하기!
            contest = get_object_or_404(ContestBoard, pk=pk)
            comment = ContestComment.objects.create(
                comment_board_no=contest,
                comment_writer=writer,
                comment_cont=contents
            )

        elif LectBoard:  # lecture 인지 구별하는 코드 생각하기!
            lecture = get_object_or_404(LectBoard, pk=pk)
            comment = LectBoardComment.objects.create(
                comment_board_no=lecture,
                comment_writer=writer,
                comment_cont=contents
            )

        if comment is not None:
            create_comment_alarm(comment)

    # 대댓글
    else:
        ref_pk = request.GET.get("comment_ref")

        if Board:  # board 인지 구별하는 코드 생각하기!
            board = get_object_or_404(Board, pk=pk)  # 게시글 번호 들고오는 것임
            comment = Comment.objects.create(
                comment_board_no=board,
                comment_writer=User.objects.get(pk=request.session.get('user_stu')),
                comment_cont=request.GET.get('comment_cont'),
                comment_cont_ref=Comment.objects.get(pk=ref_pk)
            )

        elif ContestBoard:  # contest 인지 구별하는 코드 생각하기!
            contest = get_object_or_404(ContestBoard, pk=pk)
            comment = ContestComment.objects.create(
                comment_board_no=contest,
                comment_writer=writer,
                comment_cont=contents,
                comment_cont_ref=ContestComment.objects.get(pk=ref_pk)
            )

        elif LectBoard:  # lecture 인지 구별하는 코드 생각하기!
            lecture = get_object_or_404(LectBoard, pk=pk)
            comment = LectBoardComment.objects.create(
                comment_board_no=lecture,
                comment_writer=writer,
                comment_cont=contents,
                comment_cont_ref=LectBoardComment.objects.get(pk=ref_pk)
            )

        if comment is not None:
            create_comment_ref_alarm(comment)

    comment_to_json = serializers.serialize('json', comment)
    return HttpResponse(comment_to_json, content_type="text/json-comment-filtered")


@writer_only(superuser=True)
def comment_delete(request):
    if request.method == "POST":
        comment = None
        comment_id = request.POST.get('comment_id')

        if Board:
            comment = Comment.objects.get(pk=comment_id)
        elif ContestBoard:
            comment = ContestComment.objects.get(pk=comment_id)
        elif LectBoard:
            comment = LectBoardComment.objects.get(pk=comment_id)

        comment.delete()

        return HttpResponse()


@writer_only()
def comment_update(request):
    if request.method == "POST":
        comment = None
        comment_id = request.POST.get('comment_id')

        if Board:
            comment = Comment.objects.get(pk=comment_id)
        elif ContestBoard:
            comment = ContestComment.objects.get(pk=comment_id)
        elif LectBoard:
            comment = LectBoardComment.objects.get(pk=comment_id)

        comment.comment_cont = request.POST.get("comment_cont")
        comment.save()

        comment_to_json = serializers.serialize('json', comment)
        return HttpResponse(comment_to_json, content_type="text/json-comment-filtered")


def axios_response(request):
    comments = Comment.objects.all().annotate(
        writer_name=F('comment_writer__user_name'),
        writer_major=F('comment_writer__user_major__major_name')
    ).values(
        'comment_id', 'writer_name', 'writer_major', 'comment_writer', 'comment_cont', 'comment_created',
        'comment_cont_ref'
    )

    return JsonResponse(list(comments), safe=False)

    # comments_to_json = serializers.serialize('json', comments)
    # return HttpResponse(comments_to_json, content_type="applications/json")
