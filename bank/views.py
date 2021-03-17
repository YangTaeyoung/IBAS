from django.shortcuts import render, get_object_or_404, reverse, redirect
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from DB.models import AuthUser, User, ChiefCarrier, UserRole, Board, BoardFile, \
    BoardType, Comment, History, Bank, BankFile  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from member import session
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.conf import settings
from IBAS.user_controller import is_chief_exist, is_sub_chief_exist, get_sub_chief, get_chief
import os
from IBAS.file_controller import get_filename, get_filename_with_ext

# Create your views here.
# 동아리 소개 작업할 것임
def bank_board(request):
    bank_list = Bank.objects.order_by('-bank_created').prefetch_related('bankfile_set')

    # 페이지네이터 코드
    paginator = Paginator(bank_list, 6)
    page = request.GET.get('page')
    item = paginator.get_page(page)

    return render(request, 'bank_board.html', {'bank_list' : item})
