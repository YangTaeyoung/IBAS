from django import template

register = template.Library()


# 템플릿에서 빼기 사용하려고 만듦.
@register.filter
def subtract(value, arg):
    return value - arg