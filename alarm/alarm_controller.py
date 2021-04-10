from DB.models import Alarm, Comment, User
from django.shortcuts import resolve_url


# 대댓글 대상자에게 알람 보내는 함수
# 파라미터: 등록할 댓글 객체
def create_comment_alarm(comment: Comment):
    if comment.comment_board_no.board_type_no.board_type_no == 4:  # 활동 게시판의 경우
        link = resolve_url("activity_detail", board_no=comment.comment_board_no.board_no)  # 링크를 활동 게시판 링크롤 바꿈.
    else:  # 아닐 경우
        link = resolve_url("board_detail", board_no=comment.comment_board_no.board_no)  # 일반 게시판.
    if comment.comment_writer != comment.comment_board_no.board_writer:  # 자기 게시글에 남기는 덧글은 알람을 따로 받지 않음.
        alarm = Alarm.objects.create(  # 알람 객체 생성.
            alarm_user=comment.comment_board_no.board_writer,
            alarm_cont="내 게시글에 " + comment.comment_writer.user_name + "님 께서 새로운 덧글을 남겼습니다",
            alarm_link=link
        )
        alarm.save()


# 대 댓글 대상자에게 알람을 날리는 함수.
# 파라미터: 등록할 댓글 객체
def create_comment_ref_alarm(comment: Comment):
    if comment.comment_board_no.board_type_no.board_type_no == 4:  # 활동 게시판의 경우
        link = resolve_url("activity_detail", board_no=comment.comment_board_no.board_no)  # 활동 게시판 상세로 링크 조정
    else:  # 이외의 게시판일 경우
        link = resolve_url("board_detail", board_no=comment.comment_board_no.board_no)  # 일반 게시판 상세로 링크 조정
    if comment.comment_writer != comment.comment_cont_ref.comment_writer:  # 자기 게시글은 받지 않음.
        alarm = Alarm.objects.create(  # 알람 객체 생성
            alarm_user=comment.comment_cont_ref.comment_writer,
            alarm_cont="내 덧글에 " + comment.comment_writer.user_name + "님 께서 새로운 답글을 남겼습니다",
            alarm_link=link
        )
        alarm.save()


# user: alarm을 보낼 유저 객체
def create_user_role_update_alarm(user: User):
    alarm = Alarm.objects.create(
        alarm_user=user,
        alarm_cont="회원 등급이 " + user.user_role.role_name + "으로 업데이트 되었습니다.",
        alarm_link=resolve_url("my_info")
    )
    alarm.save()


# user: alarm을 보낼 유저 객체, is_apply: 계정 승인이 막 되었을 때.
def create_user_auth_update_alarm(user: User, is_apply):
    alarm_cont = str()
    if user.user_auth.auth_no == 1:
        alarm_cont = "계정이 활성화되었습니다. 모든 기능을 사용할 수 있습니다."
    elif user.user_auth.auth_no == 2 and is_apply:
        alarm_cont = "가입이 승인되었습니다. 회비를 납부하시면 모든 기능이 활성화됩니다."
    elif user.user_auth.auth_no == 2 and not is_apply:
        alarm_cont = "계정이 비활성화되었습니다. 일부 기능이 제한됩니다."
    alarm = Alarm.objects.create(
        alarm_user=user,
        alarm_cont=alarm_cont,
        alarm_link=resolve_url("my_info")
    )
    alarm.save()
