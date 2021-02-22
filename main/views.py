from django.shortcuts import render, get_object_or_404
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from DB.models import AuthUser, User, ChiefCarrier  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from member import session

# Create your views here.

def index(request): # 메인 홈페이지 단순 이동
    return render(request, 'index.html', {})


# 탑바 작업
def index1(request):
    # 세션은 세션이 있다고 가정한 것
    session.save_session(request,User.objects.get(pk='12162359'))
    context = {}
    return render(request, "top_bar.html", context)

# 메인 작업
def index2(request):
    contest = {}
    return render(request, 'main.html', contest)

# 동아리 소개 작업할 것임
def test_activity(request):
    chief = ChiefCarrier.objects.filter(user_role=1).select_related()
    sub_chief = ChiefCarrier.objects.filter(user_role=2).select_related()
    context = {}
    return render(request, 'activity.html', context)

def index4(request):
    chief = User.objects.filter(user_role=get_object_or_404(UserRole, role_no=1))[0]
    session.save_chief(request, chief)
    return render(request, 'bottom_bar.html', {})
