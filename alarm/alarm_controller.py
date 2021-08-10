import board
from DB.models import Alarm, Comment, User, Lect, LectEnrollment, Board, UserDelete, Bank, LectBoard, ContestBoard
from django.shortcuts import resolve_url
from django.db.models import Q
from user_controller import get_logined_user


# 대댓글 대상자에게 알람 보내는 함수
# 파라미터: 등록할 댓글 객체
def create_comment_alarm(comment: Comment):
    type = comment.comment_type.comment_type_no
    init_dict = {
        "alarm_cont": f"내 게시글에 {comment.comment_writer.user_name}님이 덧글을 남겼습니다."
    }

    if type == 1:
        board = Board.objects.get(pk=comment.comment_board_ref)
        init_dict.update(
            alarm_user=board.board_writer,
            alarm_link=resolve_url("board_detail", board_no=board.board_no)
        )
    elif type == 2:
        contest_board = ContestBoard.objects.get(pk=comment.comment_board_ref)
        init_dict.update(
            alarm_user=contest_board.contest_writer,
            alarm_link=resolve_url("contest_detail", contest_no=contest_board.contest_no)
        )
    elif type == 3:
        lect_board = LectBoard.objects.get(pk=comment.comment_board_ref)
        init_dict.update(
            alarm_user=lect_board.lect_board_writer,
            alarm_link=resolve_url("lect_board_detail", room_no=lect_board.lect_no.lect_no,
                                   lect_board_no=lect_board.lect_board_no)
        )
    elif type == 4:
        user_delete = UserDelete.objects.get(pk=comment.comment_board_ref)
        init_dict.update(
            alarm_user=user_delete.suggest_user,
            alarm_cont=f"내가 발의한 제명안건에 {comment.comment_writer.user_name}님이 덧글을 남겼습니다.",
            alarm_link=resolve_url("member_delete_detail", user_delete_no=user_delete.user_delete_no)
        )
    if init_dict.get("alarm_user") != comment.comment_writer:
        Alarm.objects.create(**init_dict)

        if comment.comment_cont_ref is not None:
            if comment.comment_cont_ref.comment_writer != comment.comment_writer:
                Alarm.objects.create(
                    alarm_user=comment.comment_cont_ref.comment_writer,
                    alarm_cont=f"내 덧글에 {comment.comment_writer.user_name}님께서 덧글을 남기셨습니다.",
                    alarm_link=init_dict.get("alarm_link")
                )


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


# 관리자에 의해 게시글이 삭제되었을 때 알림
def delete_board_by_superuser_alarm(request, board: Board):
    Alarm.objects.create(
        alarm_user=board.board_writer,
        alarm_cont=get_logined_user(
            request).user_name + "님에 의해 \"" + board.board_title[:7] + "...\" 게시글이 삭제되었습니다. 운영 정책에 위반됩니다.",
        alarm_link=resolve_url("board_view", board_type_no=board.board_type_no.board_type_no)
    )


# 관리자에 의해 강의가 삭제되었을 때 알림.
def delete_lect_by_superuser_alarm(request, lect: Lect):
    lect_type = lect.lect_type.type_no
    Alarm.objects.create(
        alarm_user=lect.lect_chief,
        alarm_cont=get_logined_user(request).user_name + "님에 의해 \"" + lect.lect_title[
                                                                      :7] + "...\" 강의가 삭제되었습니다. 운영 정책에 위반됩니다.",
        alarm_link=resolve_url("lect_view", type_no=lect_type)
    )


# 관리자에 의해 강의 게시글이 삭제되었을 때 알림.
def delete_lect_board_by_superuser_alarm(request, lect_board: LectBoard):
    lect_no = lect_board.lect_no.lect_no
    Alarm.objects.create(
        alarm_user=lect_board.lect_board_writer,
        alarm_cont=get_logined_user(request).user_name + "님에 의해\"" + lect_board.lect_board_title[
                                                                     :7] + "...\" 강의가 삭제되었습니다. 운영 정책에 위반됩니다.",
        alarm_link=resolve_url("lect_room_main", room_no=lect_no)
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
            alarm_cont=user_delete.deleted_user.user_name + "님에게 제명안건이 발안되었습니다. 투표해주세요.",
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
    cfo_list = User.objects.filter(Q(user_role__role_no=4) & Q(user_auth__auth_no=1))
    for cfo in cfo_list:
        Alarm.objects.create(
            alarm_user=cfo,
            alarm_cont="새로운 예산 지원신청이 등록되었습니다.",
            alarm_link=resolve_url("bank_support_detail", bank_no=bank.bank_no)
        )


# 새로운 회원이 가입을 할 경우
def create_user_join_alarm(user: User):
    # 운영팀 이상의 회장단을 데려 옴
    chief_crews = User.objects.filter(Q(user_role__role_no__lte=3) & Q(user_auth__auth_no=1))

    for chief_crew in chief_crews:
        Alarm.objects.create(
            alarm_user=chief_crew,
            alarm_cont=user.user_name + "님이 가입 대기중입니다. 확인해주세요.",
            alarm_link=resolve_url("staff_member_list")
        )


# 회원이 회비 납부요청을 할 경우.
def create_user_activate_alarm(user: User):
    cfo_list = User.objects.filter(Q(user_role__role_no=4) & Q(user_auth__auth_no=1))
    for cfo in cfo_list:
        Alarm.objects.create(
            alarm_user=cfo,
            alarm_cont=user.user_name + "님이 회비 납부하였습니다. 확인 후, 권한을 수정해주세요.",
            alarm_link=resolve_url("staff_member_list")
        )


# 강의에서 퇴출당할 경우
def create_user_lect_out_alarm(lect_enrollment: LectEnrollment):
    Alarm.objects.create(
        alarm_user=lect_enrollment.student,
        alarm_cont=f"{lect_enrollment.lect_no.lect_chief.user_name}(강의자)님에 의해 \"{lect_enrollment.lect_no.lect_title}\" 강의에서 퇴출되었습니다.",
        alarm_link=resolve_url("index")
    )
