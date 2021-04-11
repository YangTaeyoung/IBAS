from DB.models import Alarm, User
from django.db.models import Q
from user_controller import get_logined_user, is_logined
from date_controller import today, today_before_day, today_after_day


# 사용하기 위해서는 settings.py-TEMPLATE-OPTIONS 에 각 함수를 등록 해주어야 한다.
# 사용시 그냥 일반 컨텍스트 처럼 바로 부르면 됨 예 {{ chief.user_name }}
def alarms(request):  # 알람 딕셔너리를 반환하는 함수
    if is_logined(request):
        my_alarm = Alarm.objects.filter(
            Q(alarm_user=get_logined_user(request)) & Q(
                alarm_date__range=[today_before_day(3), today_after_day(0)])).order_by("alarm_ischecked").order_by(
            "-alarm_date")
        return {
            "alarm_list": my_alarm,
            "alarm_len": len(my_alarm.filter(~Q(alarm_ischecked=1)))
        }
    else:
        return {}


def chief(request):  # 회장 정보 딕셔너리를 반환하는 함수.
    return {"chief": User.objects.filter(user_role__role_no=1).first()}
