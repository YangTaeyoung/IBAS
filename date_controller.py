from datetime import datetime, timedelta
from django.utils.dateformat import DateFormat


def today():
    return str(DateFormat(datetime.now()).format("Y-m-d h:i:s"))


def today_after_day(day):
    after = datetime.now() + timedelta(days=day)
    return after


def today_before_day(day):
    before = datetime.now() - timedelta(days=day)
    return before
