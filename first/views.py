# from django.shortcuts import render
# from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
# from .models import AuthUser  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
# 
# 
# # Create your views here.
# 
# def index(request):
#     if request.POST.get("password") is not None:  # pass페이지에서 password가 파라미터로 넘어왔을 경우에
#         print("유저 패스워드", request.POST.get("password"))  # password를 파라미터로 받음
#         user_id = AuthUser.objects.filter(password=request.POST.get("password"))[0]  # auth테이블에서 해당 패스워드가 있는지 조회.
#         print(user_id.id)
#         # 있다면 social account에서 앞서서 Auth의 primary key를 통해 가입한 친구의 pk를 넣어서 조회
#         member = SocialAccount.objects.filter(user_id=user_id.id)[0]
#         print(member)
#         # extra_data: 사용자의 동의를 통해 얻어온 권한인 듯.
#         email = member.extra_data.get('email')
#         print(email)
#         name = member.extra_data.get('name')
#         print(name)
#         return render(request, 'LightJo.html', {"email": email, "name": name})
#     print("render: LightJo")
#     return render(request, 'LightJo.html', {})
#

# def loginchk(request):
#     return render(request, 'pass_login_param.html', {})
# 
