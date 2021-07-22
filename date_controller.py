from datetime import datetime, timedelta
from django.utils.dateformat import DateFormat


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
