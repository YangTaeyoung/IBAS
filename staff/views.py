from django.shortcuts import render, reverse, redirect, get_object_or_404
from DB.models import User, UserRole, UserAuth, Answer, UserUpdateRequest, \
    UserDelete, UserDeleteAor, UserDeleteFile, UserDeleteState, \
    UserEmail, StateInfo, LectSchedule, LectMoneyStandard, UserSchedule, PolicyTerms  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from staff.forms import UserDeleteForm, UserScheduleForm, LectScheduleForm, LectMoneyStandardForm, PolicyTermsForms
from pagination_handler import get_page_object
from IBAS.forms import FileFormBase
import os
from user_controller import superuser_only, writer_only, get_logined_user, chief_only, delete_user, role_check, \
    is_default_pic, not_allowed
from django.db.models import Q, Count, Aggregate
from django.core.mail import send_mail
from django.conf import settings
from pagination_handler import get_paginator_list
from alarm.alarm_controller import create_user_auth_update_alarm, create_user_role_update_alarm, \
    create_user_delete_alarm, \
    create_finish_user_delete_alarm
from file_controller import FileController
from django.db import transaction
from django.contrib import messages
from post_controller import comment_delete_by_post_delete
from exception_handler import exist_check


# 모델에 따른 이메일 리스트를 불러오는 함수
def get_email_list(user_model):
    user_email_list = list()
    for user_email in UserEmail.objects.filter(user_stu=user_model):
        user_email_list.append(user_email.user_email)
    return user_email_list


@superuser_only(cfo_included=True)
def staff_member_list(request):
    user = get_logined_user(request)
    if user.user_role.role_no <= 4:  # 회원에 대한 관리는 회장단만
        new_user_list = User.objects.filter(Q(user_auth__auth_no=3) & Q(user_role__isnull=False)).order_by("-user_joined")  # 신입 부원 리스트
        if user.user_role.role_no == 4:  # 총무일 경우
            exist_user_list = User.objects.filter(
                ~Q(user_auth__auth_no=3) & Q(user_role__role_no=6) & Q(user_role__isnull=False))
        else:
            exist_user_list = User.objects.filter(
                ~Q(user_auth__auth_no=3) & ~Q(user_role__role_no=1) & Q(user_role__isnull=False))  # 기존 회원 리스트
            for exist_user in exist_user_list:
                if len(UserDelete.objects.filter(Q(deleted_user=exist_user) & Q(user_delete_state__state_no=1))) != 0:
                    exist_user.is_going_to_delete = True
                    exist_user.delete_no = UserDelete.objects.filter(
                        Q(deleted_user=exist_user) & Q(user_delete_state__state_no=1)).first().user_delete_no
                else:
                    exist_user.is_going_to_delete = False
                    exist_user.delete_no = 1
        exist_user_list = exist_user_list.order_by("user_auth_id", "user_role_id")
        user_update_request_list = UserUpdateRequest.objects.filter(updated_state__state_no=1)  # 이름 변경 신청을 받는 리스트
        new_user_items = get_paginator_list(request, "new_user", new_user_list, 10)
        exist_user_items = get_paginator_list(request, "exist_user", exist_user_list, 10)
        user_update_request_items = get_paginator_list(request, "request", user_update_request_list, 5)
        grade_list = list()
        for new_user in new_user_list:
            grade_list.append(new_user.user_grade)
        grade_list = list(set(grade_list))
        grade_list.sort()
        auth_list = UserAuth.objects.filter(auth_no__lte=2)  # 기존 회원은 미승인 회원으로 넘길 수 없으므로, role_no 가 2 이하인 튜플만 가져옴.
        role_list = {}
        if role_check(user, 1):  # 로그인 한 유저의 권한이 회장일 경우
            role_list = UserRole.objects.filter(~Q(role_no=5))  # 교수를 제외한 모든 유저의 권한을 조정가능.
        elif role_check(user, 2):  # 로그인 한 유저의 권한이 부회장 인 경우
            role_list = UserRole.objects.filter(Q(role_no__gt=2) & ~Q(role_no=5))  # 회장, 부회장, 교수를 제외한 유저의 권한을 조정할 수 있음.
        # 제명 리스트 받아오기 (최신 상위 5개만)
        user_delete_list = UserDelete.objects.all().order_by("-user_delete_created")[:5]
        context = {  # 컨텍스트에 등록
            "exist_user_list": exist_user_items,
            "exist_user_len": len(exist_user_list),
            "new_user_list": new_user_items,
            "new_user_len": len(new_user_list),
            "grade_list": grade_list,
            "auth_list": auth_list,
            "user_update_request_list": user_update_request_items,
            "user_delete_list": user_delete_list
        }
        if role_list:
            context.update(role_list=role_list)

        return render(request, "member_manage.html", context)  # 유저 리스트 페이지를 랜더링
    else:  # 그 외의 권한을 가진 자가 접근할 경우 (해킹 시도)
        return redirect(reverse("index"))  # 메인페이지로 보냄


@superuser_only(cfo_included=True)
def staff_member_update(request):
    if request.method == "POST":  # 파라미터가 POST로 넘어왔는가? (정상적인 접근)
        user_auth = request.POST.get("user_auth")
        user_role = request.POST.get("user_role")
        user_stu_list = request.POST.getlist("user_stu_list[]")
        print(user_stu_list)
        if user_role is None:
            user_role = -1
        if user_auth is None:
            user_auth = -1
        if (int(user_role) == 1 and len(user_stu_list) > 1) or (
                int(user_role) == 2 and len(user_stu_list) > 1):  # 회장이나 부회장으로 바꾸려고 하면서 다수의 인원을 선택했을 경우.
            messages.error(request, "꼭 한명만 선택하실 수 있습니다.")
            return redirect(reverse("staff_member_list"))  # 무효로 함. 내 정보 페이지로 이동.
        elif int(user_role) == 1 and len(user_stu_list) == 1 or (
                int(user_role) == 2 and len(user_stu_list) == 1):  # 회장 위임의 조건을 충족한 경우. (한명만 골랐을 때)
            # 기존 회장, 부회장 권한 수정 -> 일반회원
            with transaction.atomic():
                # 새로운 회장 부회장.
                cur_user = get_logined_user(request)
                if role_check(cur_user, 1, "equal"):
                    new_user = User.objects.get(pk=user_stu_list[0])  # 새로운 회장 부회장의 객체를 얻어옴.
                    new_user.user_role = UserRole.objects.get(pk=user_role)  # 권한 수정
                    new_user.user_auth = UserAuth.objects.get(pk=1)  # 회비는 납부한 것으로 가정.
                    new_user.save()
                    create_user_role_update_alarm(new_user)  # 유저의 역할이 변경되었을 때 알람을 보냄
                    create_user_auth_update_alarm(new_user, False) # 유저의 권한이 변경되었을 때 알람을 보냄. is_apply = False의 경우 비활성화 되었음을 알림.
                    if int(user_role) == 1:
                        cur_user.user_role = UserRole.objects.get(pk=6)  # 바꾸고자 하는 사람은 일반 회원으로 역할 변경됨.
                        cur_user.save()
                        create_user_role_update_alarm(cur_user)
                        return redirect(reverse("my_info"))
        else:
            for user in User.objects.all():  # 모든 유저 순회
                for user_stu in user_stu_list:  # 사용자가 권한을 바꾸기로 한 학번 리스트를 순회
                    if user.user_stu == int(user_stu):  # 만약 사용자가 선택한 학번의 친구와 기존에 유저의 학번이 일치할 경우. 즉, 사용자가 선택한 학번의 학생인 경우
                        if user_role != -1:  # 바꾸려고 한 user_role가 있는 경우(사용자가 역할을 바꾸기로 결정한 경우)
                            user.user_role = UserRole.objects.get(pk=user_role)  # 유저 역할 수정
                            if int(user_role) < 6:  # 회장단으로 승격하는 경우
                                user.user_auth = UserAuth.objects.get(pk=1)  # 회비는 납부한 것으로 가정.
                            user.save()  # DB 수정 내역 저장
                        if user_auth != -1:  # 바꾸려고 한 user_auth가 있는 경우(사용자가 권한을 바꾸기로 결정한 경우)
                            user.user_auth = UserAuth.objects.get(pk=user_auth)  # 유저 권한 수정
                            user.save()  # DB 수정 내역 저장

        return redirect(reverse("staff_member_list"))
    else:  # GET으로 넘어온 경우 비정상적인 접근.
        return redirect(reverse("index"))


# 각 멤버 질문에 대한 답변 조회하기.
@superuser_only()
def member_applications(request):
    user = User.objects.get(pk=request.POST.get('user_stu'))

    context = {
        "user": user,
        "user_answer_list": Answer.objects.filter(answer_user=user).select_related('answer_quest')
    }
    return render(request, 'member_applications.html', context)


def get_message(is_passed, user_name):  # 합/불 메시지 딕셔너리 반환
    mail_dict = dict()
    if is_passed:  # 합격할 경우
        mail_dict["mail_title"] = "[IBAS] 축하합니다. " + user_name + "님 동아리에 입부되셨습니다."
        mail_dict["mail_message"] = "안녕하세요. IBAS(Inha Bigdata Analysts Society)입니다." \
                                    "\n 저희동아리에 지원해주셔서 정말 감사드립니다." \
                                    "\nIBAS를 통해 많은 지식을 함양하고, 많은 사람과 교류하시길 바랍니다. " \
                                    "\nIBAS는 언제나 " + user_name + "님의 발전을 응원하겠습니다. " \
                                                                 "\n\n동아리에 지원해주셔서 다시 한 번 감사드립니다. IBAS에 대해 더 많은 정보를 얻고 싶다면 아래 홈페이지를 방문해주세요" \
                                                                 "\n\nIBAS 홈페이지 링크: http://www.inhabas.com"
    else:  # 불합격할 경우
        mail_dict["mail_title"] = "[IBAS]" + user_name + "님의 입부 신청 결과를 알립니다."
        mail_dict["mail_message"] = "안녕하세요. IBAS(Inha Bigdata Analysts Society)입니다." \
                                    "\n 저희동아리에 지원해주셔서 정말 감사드립니다. " \
                                    "\n안타깝게도, 내부회의 결과," + user_name + "님은 저희 동아리와 함께 할 수 없게 되었습니다." \
                                                                      "\n\nIBAS에 관심을 가져주셔서 정말 감사드립니다." \
                                                                      "\n 앞으로 " + user_name + "님의 지속적인 발전을 응원하겠습니다. \n감사합니다. -IBAS-"
    return mail_dict


# 개인 합/불 여부 수정 및 이메일 전송
def member_aor(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.POST.get("user_stu"))
        apply = int(request.POST.get("apply"))
        user_email_list = get_email_list(user)
        if apply == 1:
            # 합격 통보 이메일 메시지 딕셔너리 생성
            with transaction.atomic():
                mail_dict = get_message(True, user.user_name)
                user.user_auth = UserAuth.objects.get(pk=2)
                # 메일 전송
                send_mail(subject=mail_dict["mail_title"], message=mail_dict["mail_message"],
                          from_email=settings.EMAIL_HOST_USER, recipient_list=user_email_list)
                if user.user_role_id == 5:
                    user.user_auth = UserAuth.objects.get(pk=1)
                user.save()
                create_user_auth_update_alarm(user, True)
        else:
            # 불합격 이메일 통보 메시지 딕셔너리 생성
            with transaction.atomic():
                mail_dict = get_message(False, user.user_name)
                if not is_default_pic(str(user.user_pic)):
                    FileController.delete_all_files_of_(user)
                send_mail(subject=mail_dict["mail_title"], message=mail_dict["mail_message"],  # 메일 전송
                          from_email=settings.EMAIL_HOST_USER,
                          recipient_list=user_email_list)
                user.delete()
        return redirect(reverse("staff_member_list"))
    return redirect(reverse("index"))


def members_aor(request):  # 여러명 일괄 처리시.
    if request.method == "POST":
        user_list = User.objects.filter(user_auth__auth_no=3)
        aor = int(request.POST.get("aor"))
        if aor == 0:  # 사용자가 합격, 불합격, 아무것도 입력하지 않고 적용 버튼을 누른 경우.
            return redirect(reverse("staff_member_list"))
        for user in user_list:
            for user_stu in request.POST.getlist("user_stu_list[]"):
                if user.user_stu == int(user_stu):
                    if aor == 1:  # 합격
                        mail_dict = get_message(True, user.user_name)
                        user.user_auth = UserAuth.objects.get(pk=2)  # 비활동 회원으로 변경
                        send_mail(subject=mail_dict["mail_title"], message=mail_dict["mail_message"],  # 합격 메일 전송
                                  from_email=settings.EMAIL_HOST_USER, recipient_list=get_email_list(user))
                        if user.user_role_id == 5:
                            user.user_auth = UserAuth.objects.get(pk=1)
                        user.save()
                        create_user_auth_update_alarm(user, True)
                    else:  # 불합격
                        # 불합격 이메일 통보 메시지 딕셔너리 생성
                        mail_dict = get_message(False, user.user_name)
                        try:  # 프로필 사진 및 담았던 폴더 삭제
                            os.remove(settings.MEDIA_ROOT + "/" + str(user.user_pic))
                            os.rmdir(settings.MEDIA_ROOT + "/member/" + str(user.user_stu))
                        except FileNotFoundError:  # 파일이 존재하지 않은 경우
                            pass  # 넘어감.
                        send_mail(subject=mail_dict["mail_title"], message=mail_dict["mail_message"],  # 불합격 메일 전송
                                  from_email=settings.EMAIL_HOST_USER, recipient_list=get_email_list(user))
                        user.delete()
        return redirect(reverse("staff_member_list"))  # 처리 완료 후.
    return redirect(reverse("index"))  # 비정상적인 요청의 경우.


# 자기 자신이 투표했는지 확인
def is_voted(request, user_delete):
    return len(UserDeleteAor.objects.filter(Q(user_delete_no=user_delete) & Q(aor_user=get_logined_user(request)))) != 0


# 제명 대상인 회장 제외한 회장 전체 수 구하기
def get_valid_chief_num():
    return len(User.objects.filter(Q(user_role__role_no__lte=4) & Q(user_auth__auth_no=1))) - len(
        UserDelete.objects.filter(deleted_user__user_role__role_no__lte=4))


# 제명 안건에 참가한 리스트 구하기
def get_aor_list(user_delete):
    return UserDeleteAor.objects.filter(user_delete_no=user_delete)


# 회장단 전체가 투표했는지 확인
def is_finished(user_delete):
    return get_valid_chief_num() == len(get_aor_list(user_delete))


# 찬성이 과반이며 회장단 모두가 투표했는지 확인
def is_decided(user_delete):
    user_delete_aor_list = UserDeleteAor.objects.filter(user_delete_no=user_delete)
    return is_finished(user_delete) and len(user_delete_aor_list.filter(aor=1)) > (get_valid_chief_num() / 2)


@superuser_only(cfo_included=True)
def member_delete_list(request):
    user_delete_list = get_page_object(request, UserDelete.objects.all().order_by("user_delete_state__state_no"))
    user_delete_state_list = UserDeleteState.objects.all()
    context = {
        "user_delete_list": user_delete_list,
        "user_delete_state_list": user_delete_state_list
    }
    return render(request, "member_delete_list.html", context)


@superuser_only(cfo_included=True)
def member_delete_register(request, deleted_user):
    if deleted_user != 0:
        context = {
            "is_update": False,
            "user_delete_form": UserDeleteForm(
                initial={"deleted_user": User.objects.get(pk=deleted_user), "user_delete_state": 1}),
            "user_delete_file_form": FileFormBase()
        }
        return render(request, "member_delete_register.html", context)
    else:
        if request.method == "POST":
            user_delete_form = UserDeleteForm(request.POST)
            user_delete_file_form = FileFormBase(request.POST, request.FILES)
            if user_delete_file_form.is_valid() and user_delete_form.is_valid():
                with transaction.atomic():
                    user_delete = user_delete_form.save(suggest_user=get_logined_user(request))
                    user_delete_file_form.save(instance=user_delete)
                    create_user_delete_alarm(user_delete)
                return redirect("member_delete_detail", user_delete_no=user_delete.user_delete_no)
            return redirect(reverse("staff_member_list"))
        else:
            return redirect(reverse("index"))


@exist_check
def member_delete_detail(request, user_delete_no):
    user_delete = UserDelete.objects.get(pk=user_delete_no)
    # 제명 페이지는 일반인에게는 공개되어서는 안됨. 따라서 404페이지로 이동.
    cur_user = get_logined_user(request)
    # 해당 부분은 superuser_check로 하면 안됨. 제명 대상자가 해당 안건을 조회 가능하여야만 함.
    if not role_check(cur_user, 4, "lte") and user_delete.deleted_user != get_logined_user(request):
        return not_allowed(request, error_404=True)
    user_delete_aor_apply = UserDeleteAor.objects.filter(Q(user_delete_no=user_delete) & Q(aor=1))
    user_delete_aor_reject = UserDeleteAor.objects.filter(Q(user_delete_no=user_delete) & Q(aor=0))
    total_chief_num = len(User.objects.filter(Q(user_role__role_no__lte=4) & Q(user_auth__auth_no=1)))
    file_list, img_list, doc_list = FileController.get_images_and_files_of_(user_delete)
    context = {
        "is_writer": cur_user == user_delete.suggest_user,
        "is_voted": is_voted(request, user_delete),
        "doc_list": doc_list,
        "img_list": img_list,
        "user_delete": user_delete,
        "user_delete_aor_list": UserDeleteAor.objects.filter(user_delete_no=user_delete),
        "total_chief_num": total_chief_num,
        "is_decided": is_decided(user_delete),
    }
    if len(user_delete_aor_apply) + len(user_delete_aor_reject) != 0:
        apply_ratio = (len(UserDeleteAor.objects.filter(Q(user_delete_no=user_delete) & Q(aor=1))) / (
                len(UserDeleteAor.objects.filter(Q(user_delete_no=user_delete) & Q(aor=0))) +
                len(UserDeleteAor.objects.filter(Q(user_delete_no=user_delete) & Q(aor=1)))
        )) * 100
        apply_ratio = round(apply_ratio, 1)
        reject_ratio = 100 - apply_ratio
        context.update(apply_ratio=apply_ratio, reject_ratio=reject_ratio)
    return render(request, 'member_delete_detail.html', context)


# 일반 게시글과 다르기 때문에 관리자가 임의로 삭제할 수 없음.
@writer_only(superuser=False)
def member_delete_delete(request, user_delete_no):
    if request.method == "POST":
        user_delete = get_object_or_404(UserDelete, pk=user_delete_no)
        FileController.delete_all_files_of_(user_delete)
        comment_delete_by_post_delete(user_delete)
        user_delete.delete()
        return redirect(reverse("member_delete_list"))
    else:
        return redirect(reverse("index"))


@writer_only(superuser=False)
def member_delete_update(request, user_delete_no):
    user_delete = UserDelete.objects.get(pk=user_delete_no)
    if request.method == "GET":
        context = {
            "user_delete_form": UserDeleteForm(instance=user_delete),
            "user_delete_file_form": FileFormBase(),
            "user_delete_file_list": UserDeleteFile.objects.filter(
                file_fk=UserDelete.objects.get(pk=user_delete_no)),
            "is_update": True,
            "user_delete_no": user_delete_no
        }
        return render(request, "member_delete_register.html", context)
    else:

        user_delete_form = UserDeleteForm(request.POST)
        user_delete_file_form = FileFormBase(request.POST, request.FILES)
        user_delete_file_list = UserDeleteFile.objects.filter(file_fk=user_delete)
        if user_delete_file_form.is_valid() and user_delete_form.is_valid():
            with transaction.atomic():
                user_delete_form.update(instance=user_delete)
                FileController.remove_files_by_user(request, user_delete_file_list)
                user_delete_file_form.save(instance=user_delete)
            return redirect("member_delete_detail", user_delete_no=user_delete_no)
        else:
            redirect("member_delete_detail", user_delete_no=user_delete_no)


# 각 회장단이 찬성, 반대를 클릭했을 때
@superuser_only(cfo_included=True)
def member_delete_aor(request, user_delete_no):
    if request.method == "POST":
        user_delete = UserDelete.objects.get(pk=user_delete_no)
        # 투표하지 않은 상태에서 클릭한 경우만 반영
        if not is_voted(request, user_delete):
            UserDeleteAor.objects.create(
                user_delete_no=user_delete,
                aor_user=get_logined_user(request),
                aor=int(request.POST.get('aor')),
            )

        # 회장단 전체가 투표한 경우, 완료로 상태 변경.
        if is_finished(user_delete):
            with transaction.atomic():
                user_delete.user_delete_state = UserDeleteState.objects.get(pk=2)
                user_delete.save()
                create_finish_user_delete_alarm(user_delete)
        return redirect("member_delete_detail", user_delete_no=user_delete_no)
    return redirect("member_delete_list")


# 투표가 끝나고, 회장이 제명 버튼을 눌렀을 때.
@chief_only(vice=True)
def member_delete_decide(request, user_delete_no):
    if request.method == "POST":
        user_delete = UserDelete.objects.get(pk=user_delete_no)
        # 회장단 수와 해당 안건에 투표한 수가 동률이며 찬성이 과반수 이상인지 확인
        if is_decided(user_delete):
            delete_user(user_delete.deleted_user)
            return redirect(reverse("member_delete_list"))
        return redirect("member_delete_detail", user_delete_no=user_delete_no)
    else:  # 비정상적인 접근.
        return redirect(reverse("index"))


@chief_only(vice=True)
def user_name_update(request):
    if request.method == "POST":
        aor = int(request.POST.get('aor'))
        if aor == 0:
            return redirect(reverse('staff_member_list'))
        updated_no_list = request.POST.getlist('user_request_list[]')
        for updated_no in updated_no_list:
            user_update_request = UserUpdateRequest.objects.get(pk=updated_no)
            if aor == 3:  # 승인한 경우
                target_user = user_update_request.updated_user
                target_user.user_name = user_update_request.updated_user_name
                target_user.save()
            elif aor == 2:  # 거절한 경우
                user_update_request.updated_reject_reason = "등록된 학번과 학생 DB에 저장된 이름이 다릅니다."
            user_update_request.updated_state = StateInfo.objects.get(pk=aor)
            user_update_request.save()
    return redirect(reverse("staff_member_list"))


def get_content_of_policy_terms(type_no):
    policy_terms = PolicyTerms.objects.filter(policy_type__type_no=type_no).order_by("-policy_updated")
    if len(policy_terms) != 0:
        policy_terms = policy_terms.first()
        return {
            "policy_title": policy_terms.policy_title,
            "policy_content": policy_terms.policy_content,
            "policy_type": policy_terms.policy_type.type_no
        }
    else:
        return {
            "policy_title": "",
            "policy_content": "",
            "policy_type": type_no
        }


# 관리자 페이지
@chief_only(vice=True)
def management(request):
    max_gen = User.objects.order_by("-user_gen").first().user_gen
    lect_schedule = LectSchedule.objects.get(pk=1)
    user_schedule = UserSchedule.objects.get(pk=1)
    lect_money_standard = LectMoneyStandard.objects.get(pk=1)
    context = {
        "max_gen": max_gen,
        "lect_schedule": lect_schedule,
        "user_schedule": user_schedule,
        "lect_money_standard": lect_money_standard,
        "lect_schedule_form": LectScheduleForm(instance=lect_schedule),
        "user_schedule_form": UserScheduleForm(instance=user_schedule),
        "lect_money_standard_form": LectMoneyStandardForm(instance=lect_money_standard),
        "policy_form_1": PolicyTermsForms(initial=get_content_of_policy_terms(1), prefix='form_1'),
        "policy_form_2": PolicyTermsForms(initial=get_content_of_policy_terms(2), prefix='form_2'),
        "policy_form_3": PolicyTermsForms(initial=get_content_of_policy_terms(3), prefix='form_3')
    }
    return render(request, "management.html", context)


@chief_only()
def management_update(request, form_no):
    if request.method == "POST":
        if form_no == 1:
            user_schedule_form = UserScheduleForm(request.POST, instance=UserSchedule.objects.get(pk=1))
            if user_schedule_form.is_valid():
                user_schedule_form.save()
        elif form_no == 2:
            lect_schedule_form = LectScheduleForm(request.POST, instance=LectSchedule.objects.get(pk=1))
            if lect_schedule_form.is_valid():
                lect_schedule_form.save()
        elif form_no == 3:
            lect_money_standard_update_form = LectMoneyStandardForm(request.POST,
                                                                    instance=LectMoneyStandard.objects.get(pk=1))
            if lect_money_standard_update_form.is_valid():
                lect_money_standard_update_form.save()
        elif form_no == 4:
            policy_terms_form = PolicyTermsForms(request.POST, prefix='form_1')
            if policy_terms_form.is_valid():
                policy_terms_form.save(policy_user=get_logined_user(request))
        elif form_no == 5:
            policy_terms_form = PolicyTermsForms(request.POST, prefix='form_2')
            if policy_terms_form.is_valid():
                policy_terms_form.save(policy_user=get_logined_user(request))
        elif form_no == 6:
            policy_terms_form = PolicyTermsForms(request.POST, prefix='form_3')
            if policy_terms_form.is_valid():
                policy_terms_form.save(policy_user=get_logined_user(request))
    return redirect(reverse("management"))
