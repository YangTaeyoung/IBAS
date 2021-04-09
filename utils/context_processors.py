from DB.models import Alarm, User
from django.db.models import Q
from user_controller import get_logined_user, is_logined
from date_controller import today, today_before_day, today_after_day


def alarms(request):
    if is_logined(request):
        my_alarm = Alarm.objects.filter(
            Q(alarm_user=get_logined_user(request)) & Q(
                alarm_date__range=[today_before_day(3), today_after_day(0)])).order_by("alarm_ischecked").order_by(
            "-alarm_date")

        return {
            "alarm_list": my_alarm
        }
    else:
        return None;

def chief(request):
    return {"chief": User.objects.filter(user_role__role_no=1).first()}