from django.shortcuts import render, get_object_or_404, reverse, redirect
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from DB.models import AuthUser, User, ChiefCarrier, UserRole, Board, BoardFile, \
    BoardType, Comment, History, UserAuth, QuestForm, Answer  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from django.db.models import QuerySet
from member import session
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.conf import settings
from IBAS.user_controller import is_chief_exist, is_sub_chief_exist, get_sub_chief, get_chief
import os
from IBAS.file_controller import get_filename, get_filename_with_ext
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

def staff_member_list(request):
    if request.session.get("user_role") <= 2:  # 회원에 대한 관리는 회장과 부회장만 할 수 있음.
        member_list = User.objects.all()  # 모든 유저 리스트를 가져 옴
        context = {  # 컨텍스트에 등록
            "member_list": member_list
        }
        return render(request, "member_manage.html", context)  # 유저 리스트 페이지를 랜더링
    else:  # 그 외의 권한을 가진 자가 접근할 경우 (해킹 시도)
        return redirect(reverse("index"))  # 메인페이지로 보냄


def staff_member_update(request):
    if request.method == "POST":  # 파라미터가 POST로 넘어왔는가? (정상적인 접근)
        user_auth = request.POST.get("user_auth")
        user_role = request.POST.get("user_role")
        user_stu_list = request.POST.getlist("user_stu_list[]")
        print(user_stu_list)
        if (user_role == 1 and len(user_stu_list) > 1) or (
                user_role == 2 and len(user_stu_list) > 1):  # 회장이나 부회장으로 바꾸려고 하면서 다수의 인원을 선택했을 경우.
            return redirect(reverse("my_info"))  # 내 정보 페이지로 이동.
        elif user_role == 1 and len(user_stu_list) == 1 or (
                user_role == 2 and len(user_stu_list) == 1):  # 회장 위임의 조건을 충족한 경우. (한명만 골랐을 때)
            user = User.objects.get(pk=user_stu_list[0])
            user.user_role = UserRole.objects.get(pk=user_role)
            user.user_auth = UserAuth.objects.get(pk=1)
            user.save()
        else:
            for user in User.objects.all():  # 모든 유저 순회
                for user_stu in user_stu_list:  # 사용자가 권한을 바꾸기로 한 학번 리스트를 순회
                    if user.user_stu == int(user_stu):  # 만약 사용자가 선택한 학번의 친구와 기존에 유저의 학번이 일치할 경우. 즉, 사용자가 선택한 학번의 학생인 경우
                        print("user_stu:", user.user_stu)
                        if user_role is not None:  # 바꾸려고 한 user_role가 있는 경우(사용자가 역할을 바꾸기로 결정한 경우)
                            user.user_role = UserRole.objects.get(pk=user_role)  # 유저 역할 수정
                            if int(user_role) < 6:  # 회장단으로 승격하는 경우
                                user.user_auth = UserAuth.objects.get(pk=1)  # 회비는 납부한 것으로 가정.
                            print("user_role Change")
                            user.save()  # DB 수정 내역 저장
                        if user_auth is not None:  # 바꾸려고 한 user_auth가 있는 경우(사용자가 권한을 바꾸기로 결정한 경우)
                            user.user_auth = UserAuth.objects.get(pk=user_auth)  # 유저 권한 수정
                            print("user_auth Change")
                            user.save()  # DB 수정 내역 저장

        return redirect(reverse("my_info"))
    else:  # GET으로 넘어온 경우 비정상적인 접근.
        return redirect(reverse("index"))


def member_delete_list(request):
    context = {}
    return render(request, 'member_delete_list.html', context)


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


def member_aor(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.POST.get("user_stu"))
        apply = int(request.POST.get("apply"))
        if apply == 1:
            # 합격 통보 이메일 메시지 딕셔너리 생성
            mail_dict = get_message(True, user.user_name)
            user.user_auth = UserAuth.objects.get(pk=2)
            # 메일 전송
            send_mail(subject=mail_dict["mail_title"], message=mail_dict["mail_message"],
                      from_email=settings.EMAIL_HOST_USER, recipient_list=[user.user_email])
            user.save()
        else:
            # 불합격 이메일 통보 메시지 딕셔너리 생성
            mail_dict = get_message(False, user.user_name)
            try:
                os.remove(settings.MEDIA_ROOT + "/" + str(user.user_pic))
                os.rmdir(settings.MEDIA_ROOT + "/member/" + str(user.user_stu))
            except FileNotFoundError:
                pass
            send_mail(subject=mail_dict["mail_title"], message=mail_dict["mail_message"],  # 메일 전송
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[user.user_email])
            user.delete()
        return redirect(reverse("my_info"))
    return redirect(reverse("index"))


def members_aor(request):
    if request.method == "POST":
        user_list = User.objects.filter(user_auth__auth_no=3)
        aor = int(request.POST.get("aor"))
        if aor == 0: # 사용자가 합격, 불합격, 아무것도 입력하지 않고 적용 버튼을 누른 경우.
            return redirect(reverse("my_info"))
        for user in user_list:
            for user_stu in request.POST.getlist("user_stu_list[]"):
                if user.user_stu == user_stu:
                    if aor == 2:  # 합격
                        mail_dict = get_message(True, user.user_name)
                        user.user_auth = UserAuth.objects.get(pk=2)  # 비활동 회원으로 변경
                        send_mail(subject=mail_dict["mail_title"], message=mail_dict["mail_message"],  # 합격 메일 전송
                                  from_email=settings.EMAIL_HOST_USER, recipient_list=[user.user_email])
                        user.save()
                    else:  # 불합격
                        # 불합격 이메일 통보 메시지 딕셔너리 생성
                        mail_dict = get_message(False, user.user_name)
                        try: # 프로필 사진 및 담았던 폴더 삭제
                            os.remove(settings.MEDIA_ROOT + "/" + str(user.user_pic))
                            os.rmdir(settings.MEDIA_ROOT + "/member/" + str(user.user_stu))
                        except FileNotFoundError: # 파일이 존재하지 않은 경우
                            pass # 넘어감.
                        send_mail(subject=mail_dict["mail_title"], message=mail_dict["mail_message"],  # 불합격 메일 전송
                                  from_email=settings.EMAIL_HOST_USER, recipient_list=[user.user_email])
                        user.delete()
        return redirect(reverse("my_info"))  # 처리 완료 후.
    return redirect(reverse("index"))  # 비정상 적인 요청의 경우.


def member_delete_register(request):
    context = {}
    return render(request, 'member_delete_register.html', context)

def member_delete_detail(request):
    context = {}
    return render(request, 'member_delete_detail.html', context)
