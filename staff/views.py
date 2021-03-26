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

def member_delete_list(request):
    context = {}
    return render(request, 'member_delete_list.html', context)

def member_delete_detail(request):
    context = {}
    return render(request, 'member_delete_detail.html', context)
