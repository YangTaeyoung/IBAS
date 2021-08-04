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


# url 표시할 때, http:// 이거 나오면 구려보여서 잘르기.
@register.filter
def url(url):
    return url[url.find('w'):]


# arg 안에 tar이 포함되는지 여부를 반환하는 함수: 날짜 스트링 안에 월, 화 수 등의 키워드가 있는지 판별할 때 사용.
@register.filter
def is_exist(arg: str, tar: str):
    if arg is None:
        return False
    return arg.find(tar) != -1

