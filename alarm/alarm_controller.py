from DB.models import Alarm, Comment
from django.shortcuts import resolve_url


# 대댓글 대상자에게 알람 보내는 함수
# 파라미터: 등록할 댓글 객체
def create_comment_alarm(comment: Comment):
    print("text1")
    if comment.comment_board_no.board_type_no.board_type_no == 4:    # 활동 게시판의 경우
        link = resolve_url("activity_detail", board_no=comment.comment_board_no.board_no)   # 링크를 활동 게시판 링크롤 바꿈.
    else: # 아닐 경우
        link = resolve_url("board_detail", board_no=comment.comment_board_no.board_no)  # 일반 게시판.
    if comment.comment_writer != comment.comment_board_no.board_writer:     # 자기 게시글에 남기는 덧글은 알람을 따로 받지 않음.
        alarm = Alarm.objects.create(   # 알람 객체 생성.
            alarm_user=comment.comment_board_no.board_writer,
            alarm_cont="내 게시글에 " + comment.comment_writer.user_name + "님 께서 새로운 덧글을 남겼습니다",
            alarm_link=link
        )
        alarm.save()

# 대 댓글 대상자에게 알람을 날리는 함수.
# 파라미터: 등록할 댓글 객체
def create_comment_ref_alarm(comment: Comment):
    print("text_ref_1")
    if comment.comment_board_no.board_type_no.board_type_no == 4: # 활동 게시판의 경우
        link = resolve_url("activity_detail", board_no=comment.comment_board_no.board_no) # 활동 게시판 상세로 링크 조정
    else: # 이외의 게시판일 경우
        link = resolve_url("board_detail", board_no=comment.comment_board_no.board_no) # 일반 게시판 상세로 링크 조정
    if comment.comment_writer != comment.comment_cont_ref.comment_writer:  # 자기 게시글은 받지 않음.
        alarm = Alarm.objects.create( # 알람 객체 생성
            alarm_user=comment.comment_cont_ref.comment_writer,
            alarm_cont="내 덧글에 " + comment.comment_writer.user_name + "님 께서 새로운 답글을 남겼습니다",
            alarm_link=link
        )
        alarm.save()
