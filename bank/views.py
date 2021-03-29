from MySQLdb.converters import NoneType
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, reverse, redirect
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from DB.models import AuthUser, User, ChiefCarrier, UserRole, Board, BoardFile, \
    BoardType, Comment, History, Bank, BankFile, BankApplyInfo  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from member import session
from django.core.paginator import Paginator
from file_controller import get_file_name
from django.http import HttpResponseRedirect
from django.conf import settings
from IBAS.user_controller import is_chief_exist, is_sub_chief_exist, get_sub_chief, get_chief
import os
from IBAS.file_controller import get_filename, get_filename_with_ext


# Create your views here.
# 동아리 소개 작업할 것임
def bank(request):
    bank_list = Bank.objects.order_by('bank_used').prefetch_related('bankfile_set').all()
    year_list = list()
    for bank in bank_list:
        year_list.append(str(bank.bank_used).split('-')[0])

    year_list = list(set(year_list))
    year_list.sort()
    bank_plus = Bank.objects.all().aggregate(Sum("bank_plus"))
    bank_minus = Bank.objects.all().aggregate(Sum("bank_minus"))

    if isinstance(bank_plus["bank_plus__sum"], NoneType):
        bank_plus["bank_plus__sum"] = 0
    if isinstance(bank_minus["bank_minus__sum"], NoneType):
        bank_minus["bank_minus__sum"] = 0

    balance = bank_plus["bank_plus__sum"] - bank_minus["bank_minus__sum"]

    paginator = Paginator(bank_list, 15)  # 페이지네이터로 10개씩 보이게끔. 나중에 수정하면 됌
    page = request.GET.get('page')  # 페이지 이름 ㅇㅇ 여기서 변경하면 됌
    item = paginator.get_page(page)
    context = {
        "bank_list": item,
        "year_list": year_list,
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
                os.remove('media/' + str(file_list[i].bank_file_path))
            os.rmdir('media/bank/' + str(bank.bank_no))
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
        bank.bank_created = request.POST.get('bank_created')
        bank.bank_title = request.POST.get('bank_title')
        bank.bank_plus = request.POST.get('bank_plus')
        bank.bank_minus = request.POST.get('bank_minus')
        bank.save()
        return redirect(reverse('bank_board'))
    else:  # 비정상적인 접근의 경우 (해킹시도)
        return render(request, "index.html", {'lgn_is_failed': 1})  # 메인페이지로 보내버림


def bank_register(request):
    if request.method == "POST":
        bank_minus = 0
        bank_plus = 0
        if request.POST.get("bank_minus") != '':
            bank_minus = int(request.POST.get("bank_minus"))
        if request.POST.get("bank_plus") != '':
            bank_plus = int(request.POST.get("bank_plus"))
        bank = Bank(
            bank_used=request.POST.get('bank_used'),
            bank_title=request.POST.get('bank_title'),
            bank_reason=request.POST.get('bank_reason'),
            bank_plus=bank_plus,
            bank_minus=bank_minus,
            # cfo는 승인하는 사람인데, 처음 등록할 땐 아직 승인한 사람이 없어서 신청한 사람으로 받았음
            bank_cfo=User.objects.get(pk=request.session.get('user_stu')),
            # 사용한 사람은 user_stu 임
            bank_used_user=User.objects.get(pk=request.session.get('user_stu')),
            bank_apply=BankApplyInfo.objects.get(pk=4)  # 총무가 추가하는 경우 바로 처리됨.
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
