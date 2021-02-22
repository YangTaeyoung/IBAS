from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from DB.models import AuthUser, User  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from member import session

# Create your views here.

def index(request): # 메인 홈페이지 단순 이동
    return render(request, 'index.html', {})


# 탑바 작업중임.
def index1(request):

    # login 은 세션이 있다고 가정한 것
    session.save_session(request,User.objects.get(pk='12162359'))
    context = {}
    return render(request, "top_bar.html", context)

def index2(request):
    contest = {}
    return render(request, 'main.html', contest)