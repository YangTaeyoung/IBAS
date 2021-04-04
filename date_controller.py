from datetime import datetime
from django.utils.dateformat import DateFormat


def today():
    return str(DateFormat(datetime.now()).format("Y-m-d h:i:s"))
