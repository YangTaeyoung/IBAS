from DB.models import Alarm, Comment
from django.shortcuts import resolve_url


def create_comment_alarm(comment: Comment):
    if comment.comment_board_no.board_type_no.board_type_no == 4:
        link = resolve_url("activity_detail", board_no=comment.comment_board_no.board_no)
    else:
        link = resolve_url("board_detail", board_no=comment.comment_board_no.board_no)
    if comment.comment_writer != comment.comment_board_no.board_writer: # 자기 게시글에 남기는 덧글은 알람을 따로 받지 않음.
        Alarm.objects.create(
            alarm_user=comment.comment_board_no.board_writer,
            alarm_cont="내 게시글에" + comment.comment_writer.user_name + "님 께서 새로운 덧글을 남겼습니다",
            alarm_link=link
        )


def create_comment_ref_alarm(comment: Comment):
    if comment.comment_board_no.board_type_no.board_type_no == 4:
        link = resolve_url("activity_detail", board_no=comment.comment_board_no.board_no)
    else:
        link = resolve_url("board_detail", board_no=comment.comment_board_no.board_no)
    if comment.comment_writer != comment.comment_cont_ref.comment_writer:
        Alarm.objects.create(
            alarm_user=comment.comment_cont_ref.comment_writer,
            alarm_cont="내 덧글에" + comment.comment_writer.user_name + "님 께서 새로운 답글을 남겼습니다",
            alarm_link=link
        )
