from django import template
from file_controller import FileController

register = template.Library()


# 템플릿에서 빼기 사용하려고 만듦.
@register.filter
def subtract(value, arg):
    return value - arg


# 템플릿에서 스트링끼리 더하려고 만듦.
@register.filter
def addstr(value, arg):
    return str(value) + str(arg)


# 템플릿에서 빼기 사용하려고 만듦.
@register.filter
def get_first_img(arg):
    for file in arg:
        if FileController.is_image(file.file_path):
            return str(file.file_path)


# 글자수 length 초과하면 자르고 끝에 ... 붙임
@register.filter
def truncate(string, length):
    if len(string) < length:
        return string + ''.join([' '] * (10 - len(string)))
    else:
        return string[:length] + '...'


# url 표시할 때, http:// 이거 나오면 구려보여서 잘르기.
@register.filter
def url(url):
    return url[url.find('w'):]
