import functools
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils.dateformat import DateFormat
from DB.models import LectSchedule, UserSchedule
from user_controller import not_allowed


# 오늘을 출력 양식에 맞추어 반환
def today():
    return str(DateFormat(datetime.now()).format("Y-m-d h:i:s"))


# 오늘 datetime 객체를 반환.
def today_datetime():
    return datetime.now()


# day 이후 datetime객체를 반환
def today_after_day(day):
    after = datetime.now() + timedelta(days=day)
    return after


# day 이전 datetime 객체를 반환
def today_before_day(day):
    before = datetime.now() - timedelta(days=day)
    return before


# year 이후 datetime 객체를 반환.
def today_after_year(year):
    year = year * 365
    after = datetime.now() + timedelta(days=year)
    return after


# 회원 모집 중인지 아닌지 판단하는 함수
# OUTPUT: bool (True: 모집중임)(False:모집중 아님)
def is_user_recruiting():
    return len(
        UserSchedule.objects.filter(Q(user_register_start__lte=today()) & Q(user_register_end__gte=today()))) != 0

# 면접이 진행중인지 판단하는 함수.
def is_interview_progress():
    return len(
        UserSchedule.objects.filter(Q(user_interview_start__lte=today()) & Q(user_interview_end__gte=today()))) != 0


# 부원 모집중인지 확인하는 데코레이터
def user_recruit_check(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if is_user_recruiting():
            return func(request, *args, **kwargs)
        else:
            return not_allowed(request, msg="회원가입이 불가능합니다. 부원 모집 기간이 아닙니다.")

    return wrapper


# 강의 개설 모집 중인지 아닌지 판단하는 함수
# OUTPUT: bool (True: 모집중임)(False:모집중 아님)
def is_lect_recruiting():
    return len(
        LectSchedule.objects.filter(Q(lect_register_start__lte=today()) & Q(lect_register_end__gte=today()))) != 0


# 강의 개설 모집중인지 확인하는 데코레이터
def lect_recruit_check(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if is_lect_recruiting():
            return func(request, *args, **kwargs)
        else:
            return not_allowed(request, msg="강의 개설 허용 기간이 아닙니다.")

    return wrapper
