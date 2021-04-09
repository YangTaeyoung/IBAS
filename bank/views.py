from MySQLdb.converters import NoneType
from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404, reverse, redirect
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from DB.models import AuthUser, User, ChiefCarrier, UserRole, Board, BoardFile, \
    BoardType, Comment, History, Bank, BankFile, BankApplyInfo  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from member import session
from django.core.paginator import Paginator
from file_controller import get_file_name
from django.http import HttpResponseRedirect
from django.conf import settings
from datetime import datetime
from django.utils.dateformat import DateFormat
from IBAS.user_controller import is_chief_exist, is_sub_chief_exist, get_sub_chief, get_chief
from date_controller import today
import os
from IBAS.file_controller import get_filename, get_filename_with_ext


# Create your views here.
# 동아리 소개 작업할 것임
def bank(request):
    # 회계 내역
    bank_list = Bank.objects.filter(bank_apply__bank_apply_no=4).order_by('bank_used').prefetch_related(
        'bankfile_set').all()
    # 연도를 담을 리스트
    year_list = list()
    for bank in bank_list:
        year_list.append(str(bank.bank_used).split('-')[0])

    # 연도 리스트
    year_list = list(set(year_list))
    year_list.sort()

    # 수입, 지출 합계
    bank_plus = Bank.objects.filter(bank_apply__bank_apply_no=4).aggregate(Sum("bank_plus"))
    bank_minus = Bank.objects.filter(bank_apply__bank_apply_no=4).aggregate(Sum("bank_minus"))

    # 지출, 수입을 아직 등록하지 않은 경우의 예외처리
    if isinstance(bank_plus["bank_plus__sum"], NoneType):
        bank_plus["bank_plus__sum"] = 0
    if isinstance(bank_minus["bank_minus__sum"], NoneType):
        bank_minus["bank_minus__sum"] = 0
    # 잔액 설정
    balance = bank_plus["bank_plus__sum"] - bank_minus["bank_minus__sum"]

    # 페이지네이션 설정
    paginator = Paginator(bank_list, 15)  # 페이지네이터로 15개씩 보이게 설정
    page = request.GET.get('page')
    item = paginator.get_page(page)
    context = {
        "bank_list": item,
        "year_list": year_list,
        "bank_len": len(bank_list),
        "balance": balance
    }
    return render(request, 'bank_list.html', context)


def bank_delete(request):
    if request.method == "POST":  # 포스트로 넘어오는 경우
        bank = Bank.objects.get(pk=request.POST.get('bank_no'))
        try:
            file_list = list(BankFile.objects.filter(bank_no=bank))
            # file_list 라는 변수 선언 (여러개의 파일을 올릴 수 있으므로 list 로 변환)
            for i in range(len(file_list)):
                # file_list 의 크기 만큼 for 문으로 돌려서 파일 삭제 후 폴더 삭제
                os.remove(settings.MEDIA_ROOT + "/" + str(file_list[i].bank_file_path))
            os.rmdir(settings.MEDIA_ROOT + '/bank/' + str(bank.bank_no))
            # 파일이 안에 있는 삭제에서 폴더를 삭제할 경우 오류 만남.
        except FileNotFoundError:
            pass  # 파일이 없는 경우 그냥 통과시킨다.
        bank.delete()  # 파일과 폴더 삭제 후, 회계 DB 에서 삭제
        return redirect(reverse('bank_list'))
    else:
        return redirect(reverse('bank_list'))


def bank_update(request):
    if request.method == "POST":
        bank = Bank.objects.get(pk=request.POST.get("bank_no"))
        bank.bank_used = request.POST.get('bank_used')
        bank.bank_title = request.POST.get('bank_title')
        bank.bank_used_user = User.objects.get(pk=request.POST.get("bank_used_user"))
        bank.bank_plus = request.POST.get('bank_plus')
        bank.bank_minus = request.POST.get('bank_minus')
        bank.save()

        bank_file_list = BankFile.objects.filter(bank_no=bank)
        try:
            for bank_file in bank_file_list:
                if request.POST.get("exist_bank_file_" + str(bank_file.bank_file_id)) is None:
                    # 기존에 있던 저장소에 파일 삭제
                    os.remove(settings.MEDIA_ROOT + "/" + str(bank_file.bank_file_path))
                    # db 기록 삭제
                    bank_file.delete()
            os.rmdir(settings.MEDIA_ROOT + "/" + str(bank.bank_no))
        except FileNotFoundError:
            pass
        for updated_file in request.FILES.getlist('bank_file'):
            new_bank_file = BankFile.objects.create(bank_no=Bank.objects.get(pk=bank.bank_no),
                                                    bank_file_path=updated_file,
                                                    bank_file_name=get_file_name(updated_file))
            new_bank_file.save()
        return redirect(reverse('bank_list'))
    else:  # 비정상적인 접근의 경우 (해킹시도)
        return render(request, "index.html", {'lgn_is_failed': 1})  # 메인페이지로 보내버림


def bank_register(request):
    if request.method == "POST":
        bank_minus = 0
        bank_plus = 0
        bank_reason = request.POST.get("bank_reason")
        bank_used_user = request.POST.get("bank_used_user")
        if bank_used_user == '':
            bank_used_user = request.POST.get("bank_cfo")
        if bank_reason == '':
            bank_reason = request.POST.get("bank_title")
        if request.POST.get("bank_minus") != '':
            bank_minus = int(request.POST.get("bank_minus"))
        if request.POST.get("bank_plus") != '':
            bank_plus = int(request.POST.get("bank_plus"))
        bank = Bank.objects.create(
            bank_used=request.POST.get('bank_used'),
            bank_title=request.POST.get('bank_title'),
            bank_reason=bank_reason,
            bank_plus=bank_plus,
            bank_minus=bank_minus,
            # cfo는 승인하는 사람인데, 처음 등록할 땐 아직 승인한 사람이 없어서 신청한 사람으로 받았음
            bank_cfo=User.objects.get(pk=request.POST.get('bank_cfo')),
            # 사용한 사람은 user_stu 임
            bank_used_user=User.objects.get(pk=bank_used_user),
            bank_apply=BankApplyInfo.objects.get(pk=request.POST.get("bank_apply"))  # 총무가 추가하는 경우 바로 처리됨.
        )
        bank.save()

        for updated_file in request.FILES.getlist('bank_file'):
            new_bank_file = BankFile.objects.create(bank_no=Bank.objects.get(pk=bank.bank_no),
                                                    bank_file_path=updated_file,
                                                    bank_file_name=get_file_name(updated_file))
            new_bank_file.save()
        return redirect(reverse('bank_list'))

    else:
        return render(request, "index.html", {'lgn_is_failed': 1})


def bank_support_board(request):
    bank_list = Bank.objects.filter(~Q(bank_apply__bank_apply_no=4))
    # 페이지네이션 설정
    paginator = Paginator(bank_list, 15)  # 페이지네이터로 15개씩 보이게 설정
    page = request.GET.get('page')
    item = paginator.get_page(page)
    context = {
        "bank_list": item,
        "bank_len": len(bank_list)
    }
    return render(request, 'bank_support_board.html', context)  # 게시판 목록


def bank_support_register(request):
    context = {}
    print(request.POST.get("bank_used_user"))
    if request.method == "POST":
        bank = Bank.objects.create(
            bank_used=request.POST.get('bank_used'),
            bank_title=request.POST.get('bank_title'),
            bank_reason=request.POST.get("bank_reason"),
            bank_plus=0,
            bank_minus=request.POST.get("bank_minus"),
            bank_account=request.POST.get("bank_account"),
            # 사용한 사람은 user_stu 임
            bank_used_user=User.objects.get(pk=request.POST.get("bank_used_user")),
            bank_apply=BankApplyInfo.objects.get(pk=request.POST.get("bank_apply"))  # 총무가 추가하는 경우 바로 처리됨.
        )
        bank.save()
        for updated_file in request.FILES.getlist('bank_file'):
            new_bank_file = BankFile.objects.create(bank_no=Bank.objects.get(pk=bank.bank_no),
                                                    bank_file_path=updated_file,
                                                    bank_file_name=get_file_name(updated_file))
            new_bank_file.save()
        return redirect("bank_support_detail", bank_no=bank.bank_no)
    else:
        return render(request, 'bank_support_register.html', context)  # 등록


def bank_support_detail(request, bank_no):
    bank = Bank.objects.get(pk=bank_no)
    bank_file_list = BankFile.objects.filter(bank_no=bank)
    context = {
        "bank": bank,
        "bank_file_list": bank_file_list
    }
    return render(request, 'bank_support_detail.html', context)  # 상세보기


def bank_support_aor(request):  # 총무가 승인, 승인거절, 지급완료를 눌렀을 때의 과정
    if request.method == "POST":
        bank = Bank.objects.get(pk=request.POST.get("bank_no"))
        bank_apply_no = int(request.POST.get("bank_apply_no"))
        bank.bank_apply = BankApplyInfo.objects.get(pk=bank_apply_no)
        bank.bank_cfo = User.objects.get(pk=request.session.get('user_stu'))
        if bank_apply_no == 2:  # 승인 시
            bank.bank_checked = today()  # 검토일, 오늘
        elif bank_apply_no == 3:  # 거절 시
            bank.bank_checked = today()  # 검토일, 오늘
            bank.bank_reject_reason = request.POST.get("bank_reject_reason")
        elif bank_apply_no == 4:  # 지급 완료 시
            bank.bank_allowed = today()  # 지급 완료일, 오늘
        bank.save()
        return redirect("bank_support_detail", bank_no=bank.bank_no)
    else:
        return redirect(reverse("bank_support_board"))


def bank_support_update(request):
    if request.method == "POST":
        if request.POST.get("is_move") is not None:  # 단순 수정페이지 이동의 경우
            bank = Bank.objects.get(pk=request.POST.get("bank_no"))
            bank_file_list = BankFile.objects.filter(bank_no=bank)
            context = {
                "bank": bank,
                "bank_file_list": bank_file_list
            }
            return render(request, "bank_support_register.html", context)
        else:  # 수정을 한 후 수정 버튼을 사용자가 눌렀을 경우
            bank = Bank.objects.get(pk=request.POST.get("bank_no"))  # 객체 가져오기
            bank.bank_used = request.POST.get('bank_used'),
            bank.bank_title = request.POST.get('bank_title'),
            bank.bank_reason = request.POST.get("bank_reason"),
            bank.bank_plus = 0,
            bank.bank_minus = request.POST.get("bank_minus"),
            bank.bank_account = request.POST.get("bank_account"),
            # 사용한 사람은 user_stu 임
            bank.bank_used_user = User.objects.get(pk=request.POST.get("bank_used_user")),
            bank.save()

            bank_file_list = BankFile.objects.filter(bank_no=bank)
            try:
                for bank_file in bank_file_list:  # 기존에 파일들을 사용자가 수정할 때 삭제하는 경우
                    if request.POST.get("exist_file_path_" + str(
                            bank_file.bank_file_id)) is None:  # POST로 넘어오는 파라미터가 없는 경우 삭제를 했다고 간주함
                        # 기존에 있던 저장소에 파일 삭제
                        os.remove(settings.MEDIA_ROOT + "/" + str(bank_file.bank_file_path))
                        # db 기록 삭제
                        bank_file.delete()
                if len(BankFile.objects.filter(bank_no=bank)) == 0:  # 수정 하면서 모든 파일을 지워버린 경우.
                    os.rmdir(settings.MEDIA_ROOT + "/bank/" + str(bank.bank_no))  # 디렉토리 삭제
            except FileNotFoundError:  # 파일을 못찾았을 때 예외처리
                pass  # 존재하지 않는 것이므로 그냥 둠
            for updated_file in request.FILES.getlist('bank_file'):  # 사용자가 새롭게 추가한 파일
                new_bank_file = BankFile.objects.create(bank_no=Bank.objects.get(pk=bank.bank_no),  # 객체 생성
                                                        bank_file_path=updated_file,
                                                        bank_file_name=get_file_name(updated_file))
                new_bank_file.save()  # 새롭게 저장
        return redirect("bank_support_detail", bank_no=bank.bank_no)
    else:
        return redirect(reverse("bank_support_board"))


def bank_support_delete(request):  # 예산지원 삭제
    if request.method == "POST":  # 포스트로 넘어오는 경우
        bank = Bank.objects.get(pk=request.POST.get('bank_no'))
        try:
            file_list = list(BankFile.objects.filter(bank_no=bank))
            # file_list 라는 변수 선언 (여러개의 파일을 올릴 수 있으므로 list 로 변환)
            for i in range(len(file_list)):
                # file_list 의 크기 만큼 for 문으로 돌려서 파일 삭제 후 폴더 삭제
                os.remove(settings.MEDIA_ROOT + "/" + str(file_list[i].bank_file_path))
            os.rmdir(settings.MEDIA_ROOT + '/bank/' + str(bank.bank_no))
            # 파일이 안에 있는 삭제에서 폴더를 삭제할 경우 오류 만남.
        except FileNotFoundError:
            pass  # 파일이 없는 경우 그냥 통과시킨다.
        bank.delete()  # 파일과 폴더 삭제 후, 회계 DB 에서 삭제
        return redirect(reverse('bank_support_board'))  # 예산 지원 신청 게시판으로 이동
    else:  # get으로 넘어온 경우(해킹시도)
        return redirect(reverse('bank_support_board'))  # 삭제를 건너뛰고 예산 지원 신청 게시판으로 이동
