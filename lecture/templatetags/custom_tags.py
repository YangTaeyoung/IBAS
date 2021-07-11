from django import template

register = template.Library()


# 템플릿에서 빼기 사용하려고 만듦.
@register.filter
def subtract(value, arg):
    return value - arg


# 템플릿에서 스트링끼리 더하려고 만듦.
@register.filter
def addstr(value, arg):
    return str(value) + str(arg)


# 글자수 length 초과하면 자르고 끝에 ... 붙임
@register.filter
def truncate(string, length):
    if len(string) < length:
        return string + ''.join([' '] * (10 - len(string)))
    else:
        return string[:length] + '...'

