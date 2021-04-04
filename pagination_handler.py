from django.core.paginator import Paginator


def get_paginator_list(request, name, pg_list, num):
    paginator = Paginator(pg_list, num)  # 페이지네이터로 10개씩 보이게끔. 나중에 수정하면 됌
    page = request.GET.get(name + '_page')  # 페이지 이름 ㅇㅇ 여기서 변경하면 됌
    items = paginator.get_page(page)
    return items
