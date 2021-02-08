from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from DB.models import AuthUser  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.

# Create your views here.

def index(request):
    return render(request, 'index.html', {})


