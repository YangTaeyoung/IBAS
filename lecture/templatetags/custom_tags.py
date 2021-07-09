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