from django.shortcuts import render, get_object_or_404
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from DB.models import AuthUser, User, ChiefCarrier, UserRole, Board, BoardFile  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from member import session
from django.core.paginator import Paginator

# Create your views here.

# def index(request): # 메인 홈페이지 단순 이동
#     return render(request, 'index.html', {})


#임시 메인페이지 이동 함수
def index(request):
    context = {}
    return render(request, "index.html", context)

# 탑바 작업
def test_top_bar(request):
    # 세션은 세션이 있다고 가정한 것
    session.save_session(request,User.objects.get(pk='12162359'))

    # 세션이 없다고 가정한 것
    #request.session.clear()

    context = {}
    return render(request, "top_bar.html", context)

# 메인 작업
def test_main(request):
    context = {}
    return render(request, 'main.html', context)

# 동아리 소개 작업할 것임
def test_introduce(request):
    chief = get_object_or_404(User, user_role=1)
    sub_chief = get_object_or_404(User, user_role=2)
    context = {'chief' : chief , 'sub_chief' : sub_chief}
    return render(request, 'introduce.html', context)

def test_bottom_bar(request):
    chief = User.objects.filter(user_role=get_object_or_404(UserRole, role_no=1))[0]
    session.save_chief(request, chief)
    return render(request, 'bottom_bar.html', {})

def test_activity(request):
    board_file_list = BoardFile.objects.all()
    # board_no 와 같은 파일 경로를 가져오기 위해서 사용했음.

    # 시간 순으로 보이게끔 하려했는데 실패함.
    # if request.method == 'GET' :
    #     board_list = Board.objects.filter(board_type_no=5).order_by('board_created')
    # else:
    #     board_list = Board.objects.filter(board_type_no=5).order_by('-board_created')

    board_list = Board.objects.filter(board_type_no=5).order_by('-board_created')
    # board 에서 board_type_no = 5 인 것만 들고옴. 최신 순으로 보여주는 코드는 order_by
    # board_type_no = 5 <- 동아리게시판에 관련한 글만 가져오기 위해서 만들어짐

    paginator = Paginator(board_list, 10) # 페이지네이터로 10개씩 보이게끔. 나중에 수정하면 됌
    page = request.GET.get('page')
    item = paginator.get_page(page)

    return render(request, 'activity.html', {'board_list' : item, 'board_file_list' : board_file_list})

def test_activity_detail(request):
    if request.method == "POST":
        board_info = get_object_or_404(Board,board_no=request.POST.get('board_list')) # 번호를 들고옴
    return render(request, 'activity_detail.html', {'board_info' : board_info})

def test_activity_register(request):
    return render(request, 'activity_register.html', {})
