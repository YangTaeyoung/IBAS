from django.core.paginator import Paginator


# 1. request, 2. "페이지의 이름" 3. 페이지네이션 하고 싶은 쿼리셋 리스트 4. 페이지 네이션 숫자. 몇 개씩 한 페이지에 보이게 할 것인지.
def get_paginator_list(request, name, pg_list, num):
    paginator = Paginator(pg_list, num)  # 페이지네이터로 10개씩 보이게끔. 나중에 수정하면 됌
    page = request.GET.get(name + '_page')  # 페이지 이름 ㅇㅇ 여기서 변경하면 됌
    items = paginator.get_page(page)
    return items
