from django.shortcuts import render, get_object_or_404, reverse, redirect
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from DB.models import AuthUser, User, ChiefCarrier, UserRole, Board, BoardFile, \
    BoardType, Comment, History  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
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
    context = {}
    return render(request, 'bank_board.html', context)  # introduce 에 실어서 보내분다.

def bank_support_list(request):
    context = {}
    return render(request, 'bank_support_list.html', context)  #게시판 목록

def bank_support_register(request):
    context = {}
    return render(request, 'bank_support_register.html', context) #등록

def bank_support_detail(request):
    context = {}
    return render(request, 'bank_support_detail.html', context)  #상세보기
