from django.shortcuts import render, get_object_or_404,redirect,reverse
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from DB.models import AuthUser, User, ChiefCarrier, UserRole, Board, BoardFile, \
    BoardType  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from member import session
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
import os


# 메인페이지 이동 함수
def index(request):

    if len(User.objects.filter(user_role=1)) != 0:  # 회장정보가 유저 DB에 존재하는 경우
        chief = User.objects.filter(user_role=1)[0]  # 회장의 역할(1) 인 사람의 객채를 가져옴
        session.save_chief(chief)
    return render(request, "index.html", {})



# 동아리 소개 작업할 것임
def test_introduce(request):
    chief = get_object_or_404(User, user_role=1)  # 회장의 역할(1) 인 사람의 객채를 가져옴
    sub_chief = get_object_or_404(User, user_role=2)  # 부회장의 역할(2) 인 사람의 객체를 가져옴
    context = {'chief': chief, 'sub_chief': sub_chief}  # context 에 넣어준다.
    return render(request, 'introduce.html', context)  # introduce 에 실어서 보내분다.

# 동아리 활동 게시판
def test_activity(request):
    board_file_list = BoardFile.objects.all()
    # board_no 와 같은 파일 경로를 가져오기 위해서 사용했음.

    board_list = Board.objects.filter(board_type_no=5).order_by('-board_created')
    # board 에서 board_type_no = 5 인 것만 들고옴. 최신 순으로 보여주는 코드는 order_by
    # board_type_no = 5 <- 동아리게시판에 관련한 글만 가져오기 위해서 만들어짐

    paginator = Paginator(board_list, 10)  # 페이지네이터로 10개씩 보이게끔. 나중에 수정하면 됌
    page = request.GET.get('page')  # 페이지 이름 ㅇㅇ 여기서 변경하면 됌
    item = paginator.get_page(page)

    return render(request, 'activity.html', {'board_list': item, 'board_file_list': board_file_list})


# 동아리 활동 게시판 상세보기
def test_activity_detail(request):
    if request.method == "POST":  # 자세히 보기를 하면
        board_info = get_object_or_404(Board, board_no=request.POST.get('board_list'))  # 게시글 번호로 게시글 내용을 들고옴
        return render(request, 'activity_detail.html', {'board_info': board_info})
    else:  # 파라미터가 제대로 넘어오지 않은 경우, 즉 비정상적인 경로를 통해 들어간 경우 바로 나오게 해준다.
        return HttpResponseRedirect('/test/test_activity/')

# 동아리 활동 등록하기
def test_activity_register(request):

    # 글쓰기 들어와서 등록 버튼을 누르면 실행이 되는 부분
    if request.method == "POST":
        type_no = BoardType.objects.get(pk=5) # 동아리 활동 게시판이므로 pk=5임
        user_stu = User.objects.get(pk=request.session.get('user_stu')) # 유저 학번 들고오는 것임

        activity_register = Board( # 객체로 저장을 할 것이오
            board_type_no=type_no,
            board_title=request.POST.get('activity_title'),
            board_cont=request.POST.get('activity_cont'),
            board_writer=user_stu)
        activity_register.save() # DB 에 차곡차곡 저장을 함

        # ============================= 이미지 저장시키는 코드 =========================
        for img in request.FILES.getlist('activity_file'):
            board_file = BoardFile() # 객체 생성
            board_file.board_no = Board.objects.get(pk=activity_register.board_no) # FK 키 가져오기
            board_file.board_file_path = img # 파일 경로 넣어주고
            board_file.save() # DB 에 저장 시켜줌
            # 여기서, pk 는 auto_incre 라서 상관 X

        return redirect(reverse("test_activity"))

    # POST가 아닌 그냥 보여주는 방식
    return render(request, 'activity_register.html', {})

def test_activity_delete(request):
    if request.method == "POST":
        activity = get_object_or_404(Board, pk=request.POST.get('board_no'))

        try :
            os.remove('media/'+str(BoardFile.objects.get(board_no=activity.board_no).board_file_path))
        except FileNotFoundError:
            pass

        activity.delete()
        return HttpResponseRedirect('/test/test_activity/')

    else:  # 파라미터가 제대로 넘어오지 않은 경우, 즉 비정상적인 경로를 통해 들어간 경우 바로 나오게 해준다.
        return HttpResponseRedirect('/test/test_activity/')

def test_activity_v1(request):  # 입부신청 완료 페이지로 이동
    return render(request, 'test_activity_v1.html', {})

def activity_comment(request):
    return HttpResponseRedirect('/test/test_activity/detail/')
    # return render(request, 'activity_detail.html', {})