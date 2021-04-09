from DB.models import Alarm, User
from user_controller import get_logined_user


def alarms(request):
    return {"alarm_list": Alarm.objects.filter(alarm_user=User.objects.get(pk=get_logined_user(request)))}
