from django.shortcuts import render, redirect
from django.http import HttpResponse
from allauth.socialaccount.models import SocialAccount
from .models import AuthUser


# Create your views here.

def index(request):
    if request.GET.get("password") is not None:
        print("유저 패스워드", request.GET.get("password"))
        user_id = AuthUser.objects.filter(password=request.GET.get("password"))[0]
        print(user_id.id)
        member = SocialAccount.objects.filter(user_id=user_id.id)[0]
        print(member)
        email = member.extra_data['email']
        print(email)
        name = member.extra_data['name']
        print(name)
        return render(request, 'LightJo.html', {"email": email, "name": name})
    print("왔냐?2")
    return render(request, 'LightJo.html', {})


def loginchk(request):
    return render(request, 'pass_login_param.html', {})


1
