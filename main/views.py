from django.shortcuts import render, get_object_or_404
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from DB.models import AuthUser, User, ChiefCarrier, UserRole, Board, BoardFile, \
    BoardType  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from member import session
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect


# Create your views here.

# def index(request): # 메인 홈페이지 단순 이동 # 이거 사용 안하는 중
#     return render(request, 'index.html', {})


# 탑바 작업
def test_top_bar(request):
    # 세션은 세션이 있다고 가정한 것
    session.save_session(request, User.objects.get(pk='12162359'))

    # 세션이 없다고 가정한 것
    # request.session.clear()

    context = {}
    return render(request, "top_bar.html", context)


# 메인 작업
def test_main(request):
    context = {}  # 메인은 가져올 게 없음
    return render(request, 'main.html', context)


# 동아리 소개 작업할 것임
def test_introduce(request):
    chief = get_object_or_404(User, user_role=1)  # 회장의 역할(1) 인 사람의 객채를 가져옴
    sub_chief = get_object_or_404(User, user_role=2)  # 부회장의 역할(2) 인 사람의 객체를 가져옴
    context = {'chief': chief, 'sub_chief': sub_chief}  # context 에 넣어준다.
    return render(request, 'introduce.html', context)  # introduce 에 실어서 보내분다.


def test_bottom_bar(request):
    chief = User.objects.filter(user_role=get_object_or_404(UserRole, role_no=1))[0]  # 하단바에서 회장꺼만 들고오면 됌
    session.save_chief(request, chief)  # 회장꺼 세션에 저장시켜줬음. save_chief 함수는 session 에 있음.
    return render(request, 'bottom_bar.html', {})  # 세션만 적용하는 거라 딱히 보내줄 게 없음


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

    paginator = Paginator(board_list, 10)  # 페이지네이터로 10개씩 보이게끔. 나중에 수정하면 됌
    page = request.GET.get('page')  # 페이지 이름 ㅇㅇ 여기서 변경하면 됌
    item = paginator.get_page(page)

    return render(request, 'activity.html', {'board_list': item, 'board_file_list': board_file_list})


def test_activity_detail(request):  # 자세히 보기를 위함
    if request.method == "POST":  # 자세히 보기를 하면
        board_info = get_object_or_404(Board, board_no=request.POST.get('board_list'))  # 게시글 번호로 게시글 내용을 들고옴
        return render(request, 'activity_detail.html', {'board_info': board_info})
    else:  # 파라미터가 제대로 넘어오지 않은 경우, 즉 비정상적인 경로를 통해 들어간 경우 바로 나오게 해준다.
        return HttpResponseRedirect('/test/test_activity/')


def test_activity_register(request):
    if request.method == "POST":
        type_no = BoardType.objects.get(pk=5)
        user_stu = User.objects.get(pk=request.session.get('user_stu'))

        activity_register = Board(
            board_type_no=type_no,
            board_title=request.POST.get('activity_title'),
            board_cont=request.POST.get('activity_cont'),
            board_writer=user_stu)
        activity_register.save()

        # activity_register = {
        #     'board_type_no' : 5,
        #     'board_title' : request.POST.get('activity_title') ,
        #     'board_cont' : request.POST.get('activity_cont'),
        #     'board_writer' : request.session.get('user_stu'),
        # }
        # activity_register

    return render(request, 'activity_register.html', {})
