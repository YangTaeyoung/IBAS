from django.shortcuts import render, get_object_or_404, reverse, redirect
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from DB.models import AuthUser, User, ChiefCarrier, UserRole, Board, BoardFile, \
    BoardType, Comment  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from member import session
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
import os


# 메인페이지 이동 함수
def index(request):
    if len(User.objects.filter(user_role=get_object_or_404(UserRole, role_no=1))) != 0:
        chief = User.objects.filter(user_role=get_object_or_404(UserRole, role_no=1))[0]  # 하단바에서 회장꺼만 들고오면 됌
        session.save_chief(request, chief)  # 회장꺼 세션에 저장시켜줬음. save_chief 함수는 session 에 있음.
    context = {}
    return render(request, "index.html", context)


# 동아리 소개 작업할 것임
def introduce(request):
    context = {}
    if len(User.objects.filter(user_role=1)) != 0 and len(User.objects.filter(user_role=2)) != 0:
        chief = get_object_or_404(User, user_role=1)  # 회장의 역할(1) 인 사람의 객채를 가져옴
        sub_chief = get_object_or_404(User, user_role=2)  # 부회장의 역할(2) 인 사람의 객체를 가져옴
        context = {'chief': chief, 'sub_chief': sub_chief}  # context 에 넣어준다.
    return render(request, 'introduce.html', context)  # introduce 에 실어서 보내분다.


# 동아리 활동 게시판
def activity(request):
    # 최신순으로 정렬하고, 1:M 관계로 가져오기 위해 prefetch_related 함수 사용
    board_list = Board.objects.order_by('-board_created').prefetch_related("boardfile_set")
    # board 에서 board_type_no = 5 인 것만 들고옴. 최신 순으로 보여주는 코드는 order_by
    # board_type_no = 5 <- 동아리게시판에 관련한 글만 가져오기 위해서 만들어짐
    paginator = Paginator(board_list, 6)  # 페이지네이터로 10개씩 보이게끔. 나중에 수정하면 됌
    page = request.GET.get('page')  # 페이지 이름 ㅇㅇ 여기서 변경하면 됌
    item = paginator.get_page(page)

    return render(request, 'activity.html', {'board_list': item})


# 동아리 활동 게시판 상세보기
def activity_detail(request):
    if request.method == "POST":  # 자세히 보기를 하면
        board_info = get_object_or_404(Board, board_no=request.POST.get('board_list'))  # 게시글 번호로 게시글 내용을 들고옴
        comment_info = Comment.objects.filter(comment_board_no=request.POST.get('board_list')).prefetch_related("comment_cont_ref") # 게시글 번호로 댓글 내용

        return render(request, 'activity_detail.html', {'board_info': board_info, 'comment_info': comment_info})
    else:  # 파라미터가 제대로 넘어오지 않은 경우, 즉 비정상적인 경로를 통해 들어간 경우 바로 나오게 해준다.
        return redirect(reverse('activity'))


# 동아리 활동 등록하기
def activity_register(request):
    # 글쓰기 들어와서 등록 버튼을 누르면 실행이 되는 부분
    if request.method == "POST":
        activity = Board(  # 객체로 저장을 할 것이오
            board_type_no=BoardType.objects.get(pk=5),
            board_title=request.POST.get('activity_title'),
            board_cont=request.POST.get('activity_cont'),
            board_writer=User.objects.get(pk=request.session.get('user_stu'))  # 유저 학번 들고오는 것임
        )
        activity.save()  # DB 에 차곡차곡 저장을 함

        # ============================= 이미지 저장시키는 코드 =========================
        for activity_file in request.FILES.getlist('activity_file'):
            board_file = BoardFile.objects.create(
                board_no=activity,  # FK 키 가져오기
                board_file_path=activity_file,
            )  # 객체 생성
            board_file.save()  # DB 에 저장 시켜줌
            # 여기서, pk 는 auto_incre 라서 상관 X
        print(request.FILES.getlist('activity_file'))
        return redirect(reverse("activity"))

    # POST가 아닌 그냥 보여주는 방식
    return render(request, 'activity_register.html', {})


# 동아리 활동 상세페이지에서 삭제하는 코드
def activity_delete(request):
    if request.method == "POST":  # 포스트로 넘어오는 경우
        activity = get_object_or_404(Board, pk=request.POST.get('board_no'))
        try:
            file_list = list(BoardFile.objects.filter(board_no=activity.board_no))
            # file_list 라는 변수 선언 (여러개의 파일을 올릴 수 있으므로 list 로 변환)
            for i in range(len(file_list)):
                # file_list 의 크기 만큼 for 문으로 돌려서 파일 삭제 후 폴더 삭제
                os.remove('media/' + str(file_list[i].board_file_path))
            os.rmdir('media/board/' + str(activity.board_no))
            # 파일이 안에 있는 삭제에서 폴더를 삭제할 경우 오류 만남.
        except FileNotFoundError:
            pass  # 파일이 없는 경우 그냥 통과시킨다.

        activity.delete()  # 파일과 폴더 삭제 후, 게시글 DB 에서 삭제
        return redirect(reverse('activity'))

    else:  # 파라미터가 제대로 넘어오지 않은 경우, 즉 비정상적인 경로를 통해 들어간 경우 바로 나오게 해준다.
        return redirect(reverse('activity'))


# 댓글 달기 코드
def activity_comment(request):
    if request.method == "GET":
        user_stu = User.objects.get(pk=request.session.get('user_stu'))  # 유저 학번 들고오는 것임
        board_no = Board.objects.get(pk=request.GET.get('board_no'))  # 게시글 번호 들고오는 것임

        # 객체로 받아서 저장할 예정
        comment_register = Comment(
            comment_board_no=board_no,
            comment_writer=user_stu,
            comment_cont=request.GET.get('activity_comment')
        )
        comment_register.save()
        # 데이터 베이스에 저장
        return redirect(reverse('activity_detail'))
    return redirect(reverse('activity_detail'))


# 댓글 삭제 코드
def activity_comment_delete(request):
    if request.method == "POST":  # 댓글 삭제를 누를 경우
        comment = get_object_or_404(Comment, pk=request.POST.get('comment_id'))
        # 그 댓글의 pk 를 찾아서 DB 에서 지운다.
        comment.delete()
        return redirect(reverse('activity_detail'))  # 수정 해야 함.
    # 비정상적인 경로를 통해 들어간 경우 바로 나오게 해준다.
    return redirect(reverse('activity_detail'))

# 댓글 수정 코드
def activity_comment_update(request):
    if request.method == "POST": # 정상적으로 파라미터가 넘어왔을 경우
        comment = get_object_or_404(Comment, pk=request.POST.get('comment_id')) # 가져온 comment_id를 토대로 수정 내역을 적용

        # 필요하면 사용하려고 복붙함
        # user_stu = User.objects.get(pk=request.session.get('user_stu'))  # 유저 학번 들고오는 것임
        # board_no = Board.objects.get(pk=request.POST.get('board_no'))  # 게시글 번호 들고오는 것임

        comment.comment_cont = request.POST.get('comment_cont') # 수정할 내용을 가져옴
        # comment.save() # DB 저장
        #return redirect(reverse('activity_detail'))

    return redirect(reverse('activity'))


# 동아리 글 수정 코드
def activity_update(request):
    # 수정을 누르면 GET 방식으로 DB 에 있는 것을 꺼내 온다.
    if request.method == "GET":
        item = get_object_or_404(Board, pk=request.GET.get('board_no'))  # 맞는 것을 가져온다.
        return render(request, 'activity_register.html', {'item': item})  # 이거로 보내줘서 작업 가능

    # 수정을 하고 난 후 수정 버튼을 누를 경우 이걸로 진행 됌
    if request.method == 'POST':
        return redirect(reverse("activity"))

    # 잘못 왔을 경우
    return render(request, 'activity.html', {})


def activity_detail_v1(request):
    return render(request, 'activity_detail_v1.html', {})
