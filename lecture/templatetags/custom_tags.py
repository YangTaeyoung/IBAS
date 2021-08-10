from django import template
from file_controller import FileController
from user_controller import get_logined_user

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
    return url[url.find('/') + 2:]

# 글자수 length 초과하면 자르고 끝에 ... 붙임
@register.filter
def truncate(string, length):
    if len(string) < length:
        return string + ''.join([' '] * (10 - len(string)))
    else:
        return string[:length] + '...'


# arg 안에 tar이 포함되는지 여부를 반환하는 함수: 날짜 스트링 안에 월, 화 수 등의 키워드가 있는지 판별할 때 사용.
@register.filter
def is_exist(arg: str, tar: str):
    if arg is None:
        return False
    return arg.find(tar) != -1


# 이름이나 학번 가림.
@register.simple_tag
def personal_info(string, request, lect):
    cur_user = get_logined_user(request)

    if cur_user == lect.lect_chief:
        return string

    elif cur_user.user_role_id <= 3:
        # 학번 : 1217****
        if type(string) == int:
            return str(string)[:4] + '****'
        else:
            string = str(string)
            # 학과는 '학과'만 표시
            if '학과' in string:
                return '*' * len(string[:-2]) + '학과'

            # 전화번호
            elif '-' in string:
                return string[:3] + '-****-****'

            else:
                # 이메일
                if '@' in string:
                    return '*' * string.find('@') + string[string.find('@'):]
                # 이름 : 성만 표기
                else:
                    return string[0] + '*' * (len(string) - 1)



