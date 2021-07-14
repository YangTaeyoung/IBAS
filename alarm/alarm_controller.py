from DB.models import Alarm, Comment, User, Lect, LectEnrollment, Board, UserDelete, Bank
from django.shortcuts import resolve_url
from django.db.models import Q


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


# 강의 등록이 가득 찼을 때 띄우는 알림
def create_lect_full_alarm(lect: Lect):
    if len(LectEnrollment.objects.filter(lect_no=lect)) == lect.lect_limit_num:
        Alarm.objects.create(
            alarm_user=lect.lect_chief,
            alarm_cont="개설하신 " + lect.lect_title + lect.lect_type.type_name + "(이)가 가득 찼습니다.",
            alarm_link=resolve_url("lect_detail", lect_no=lect.lect_no)
        )


# 강의 등록이 성공하였을 때 띄우는 알림(학생관점)
def create_lect_enroll_alarm(lect_enroll: LectEnrollment):
    Alarm.objects.create(
        alarm_user=lect_enroll.student,
        alarm_cont=lect_enroll.lect_no.lect_title + lect_enroll.lect_no.lect_type.type_name + "에 성공적으로 등록되었습니다.",
        alarm_link=resolve_url("lect_detail", lect_no=lect_enroll.lect_no.lect_no)
    )


# 공지사항이 올라갈 시 전체 알림
def create_board_notice_alarm(board: Board):
    if board.board_type_no.board_type_no == 1:
        user_list = User.objects.filter(~Q(user_stu=board.board_writer.user_stu))
        for user in user_list:
            Alarm.objects.create(
                alarm_user=user,
                alarm_cont="새로운 공지사항이 등록되었습니다.",
                alarm_link=resolve_url("board_detail", board_no=board.board_no)
            )


# 제명 안건이 올라왔을 때
def create_user_delete_alarm(user_delete: UserDelete):
    Alarm.objects.create(
        alarm_user=user_delete.deleted_user,
        alarm_cont="귀하에게 제명 안건이 발안되었습니다.",
        alarm_link=resolve_url("member_delete_detail", user_delete_no=user_delete.user_delete_no)
    )

    chief_list = User.objects.filter(Q(user_role__role_no__lte=4) & ~Q(user_stu=user_delete.deleted_user.user_stu) & ~Q(
        user_stu=user_delete.suggest_user.user_stu))
    for chief in chief_list:
        Alarm.objects.create(
            alarm_user=chief,
            alarm_cont=user_delete.suggest_user.user_name + "님에게 제명안건이 발안되었습니다. 투표해주세요.",
            alarm_link=resolve_url("member_delete_detail", user_delete_no=user_delete.user_delete_no)
        )


# 제명 안건이 가결되었을 때
def create_finish_user_delete_alarm(user_delete: UserDelete):
    Alarm.objects.create(
        alarm_user=User.objects.filter(Q(user_role__role_no=1) & Q(user_auth__auth_no=1)).first(),
        alarm_cont=user_delete.deleted_user.user_name + "님 앞으로 발안된 제명안건이 가결되었습니다. 제명 버튼이 활성화됩니다.",
        alarm_link=resolve_url("member_delete_detail", user_delete_no=user_delete.user_delete_no)
    )


# 예산 지원신청을 넣었을 때
def create_bank_alarm(bank: Bank):
    cfo_list = User.objects.filter(user_role__role_no=4)
    for cfo in cfo_list:
        Alarm.objects.create(
            alarm_user=cfo,
            alarm_cont="새로운 예산 지원신청이 등록되었습니다.",
            alarm_link=resolve_url("bank_support_detail", bank_no=bank.bank_no)
        )

