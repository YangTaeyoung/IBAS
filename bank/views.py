from MySQLdb.converters import NoneType
from django.db import transaction
from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404, reverse, redirect
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from DB.models import AuthUser, User, ChiefCarrier, UserRole, Board, BoardFile, \
    BoardType, Comment, History, Bank, BankFile, BankApplyInfo  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from bank.forms import BankForm, FileForm, BankSupportForm
from member import session
from django.core.paginator import Paginator

from django.http import HttpResponseRedirect
from django.conf import settings
from datetime import datetime
from django.utils.dateformat import DateFormat
from date_controller import today
import os
from file_controller import FileController
from pagination_handler import get_page_object
from user_controller import is_logined, login_required, get_logined_user


# Create your views here.
# 동아리 소개 작업할 것임
@login_required
def bank(request):
    # 회계 내역
    bank_list = Bank.objects.filter(bank_apply__bank_apply_no=4).order_by('bank_used').prefetch_related(
        'bankfile_set').all()

    # 연도를 담을 리스트
    year_list = [bank.bank_used.year for bank in bank_list]
    year_list = list(set(year_list))
    year_list.sort()

    # 수입, 지출 합계
    total_income = Bank.objects.filter(bank_apply__bank_apply_no=4).aggregate(Sum("bank_plus"))["bank_plus__sum"]
    total_outcome = Bank.objects.filter(bank_apply__bank_apply_no=4).aggregate(Sum("bank_minus"))["bank_minus__sum"]
    balance = total_income - total_outcome

    # 페이지네이션 설정
    item = get_page_object(request, bank_list, 15)  # 페이지네이션 15개씩 보이게 설정

    # 폼 객체
    bank_form = BankForm()
    file_form = FileForm()
    context = {
        "bank_list": item,
        "year_list": year_list,
        "balance": balance,
        'bank_form': bank_form,
        'file_form': file_form,
    }

    return render(request, 'bank_list.html', context)


@login_required
def bank_delete(request):
    if request.method == "POST":  # 포스트로 넘어오는 경우
        bank = get_object_or_404(Bank, pk=request.POST.get('bank_no'))
        FileController.delete_all_files_of_(bank)
        bank.delete()  # 파일과 폴더 삭제 후, 회계 DB 에서 삭제

        return redirect(reverse('bank_list'))

    return redirect(reverse("index"))


@login_required
def bank_update(request):
    if request.method == "POST":
        bank = get_object_or_404(Bank, pk=request.POST.get("bank_no"))
        bank_form = BankForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if bank_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                bank_form.update(instance=bank)
                file_form.save(instance=bank)
                band_files = BankFile.objects.filter(bank_no=bank)  # 게시글 파일을 불러옴
                FileController.remove_files_by_user(request, band_files)  # 사용자가 삭제한 파일을 제거

        return redirect(reverse('bank_list'))
    else:  # 비정상적인 접근의 경우 (해킹시도)
        return redirect(reverse("index"))  # 메인페이지로 보내버림


@login_required
def bank_register(request):
    if request.method == "POST":
        bank_form = BankForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if bank_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                bank = bank_form.save(bank_cfo=get_logined_user(request))
                file_form.save(instance=bank)
        else:
            pass  # 오류처리 필요

        return redirect(reverse('bank_list'))

    else:
        return redirect(reverse("index"))


@login_required
def bank_support_board(request):
    bank_list = Bank.objects.filter(~Q(bank_apply__bank_apply_no=4))

    # 페이지네이터 설정
    item = get_page_object(request, bank_list, 15)  # 페이지네이션 15개씩 보이게 설정

    context = {
        "bank_list": item,
        "bank_len": len(bank_list)
    }

    return render(request, 'bank_support_board.html', context)  # 게시판 목록


@login_required
def bank_support_register(request):
    if request.method == "POST":
        bank_support_form = BankSupportForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if bank_support_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                bank = bank_support_form.save(user=get_logined_user(request))
                file_form.save(instance=bank)

        return redirect("bank_support_detail", bank_no=bank.bank_no)

    elif request.method == 'GET':
        context = {
            'bank_support_form': BankSupportForm(),
            'file_form':  FileForm()
        }
        return render(request, 'bank_support_register.html', context)


@login_required
def bank_support_detail(request, bank_no):
    bank = get_object_or_404(Bank, pk=bank_no)
    bank_file_list = BankFile.objects.filter(bank_no=bank)
    context = {
        "bank": bank,
        "bank_file_list": bank_file_list
    }

    return render(request, 'bank_support_detail.html', context)  # 상세보기



@login_required
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
        if is_logined(request):
            return redirect(reverse("bank_support_board"))
        else:
            return redirect(reverse("index"))


@login_required
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
                                                        bank_file_name=updated_file.name)
                new_bank_file.save()  # 새롭게 저장
        return redirect("bank_support_detail", bank_no=bank.bank_no)
    else:
        if is_logined(reverse("index")):
            return redirect(reverse("bank_support_board"))
        else:
            return redirect(reverse("index"))


@login_required
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
        if is_logined(request):
            return redirect(reverse('bank_support_board'))  # 삭제를 건너뛰고 예산 지원 신청 게시판으로 이동
        else:
            return redirect(reverse("index"))
