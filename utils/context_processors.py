from DB.models import Alarm, User, PolicyTerms
from django.db.models import Q
from user_controller import get_logined_user, is_logined, role_check
from date_controller import today, today_before_day, today_after_day


# 사용하기 위해서는 settings.py-TEMPLATE-OPTIONS 에 각 함수를 등록 해주어야 한다.
# 사용시 그냥 일반 컨텍스트 처럼 바로 부르면 됨 예 {{ chief.user_name }}

# 알람 딕셔너리를 반환하는 함수
def alarms(request):
    if is_logined(request):
        my_alarm = Alarm.objects.filter(
            Q(alarm_user=get_logined_user(request)) & Q(
                alarm_date__range=[today_before_day(3), today_after_day(0)])).order_by("alarm_ischecked", "-alarm_date")
        return {
            "alarm_list": my_alarm,
            "alarm_len": len(my_alarm.filter(~Q(alarm_ischecked=1)))
        }
    else:
        return {}


# 회장 정보 딕셔너리를 반환하는 함수.
def chief(request):
    return {"chief": User.objects.filter(user_role__role_no=1).first()}


# 로그인을 시키는 함수.
def login(request):
    if is_logined(request):
        return {"logined_user": get_logined_user(request)}
    else:
        return {}


# 로그인 확인 정보를 컨텍스트에 등록하는 함수.
def login_check(request):
    return {"is_logined": is_logined(request)}


# 활동 회원인지 확인하는 함수.
def is_active(request):
    if is_logined(request):
        return {"is_active": get_logined_user(request).user_auth.auth_no == 1}
    else:
        return {}


# 로그인한 유저가 관리자인지 확인하는 함수
def superuser_check(request):
    if is_logined(request):
        return {"is_superuser": role_check(get_logined_user(request), 3, "lte")}
    else:
        return {"is_superuser": False}


# 로그인 한 유저가 총무인지 확인하는 함수.
def cfo_check(request):
    if is_logined(request):
        return {"is_cfo": get_logined_user(request).user_role.role_no == 4}
    else:
        return {"is_cfo": False}


def get_policies(request):
    return {
        "policy_type_1": PolicyTerms.objects.filter(policy_type__type_no=1).order_by("-policy_updated").first(),
        "policy_type_2": PolicyTerms.objects.filter(policy_type__type_no=2).order_by("-policy_updated").first(),
        "policy_type_3": PolicyTerms.objects.filter(policy_type__type_no=3).order_by("-policy_updated").first()
    }
