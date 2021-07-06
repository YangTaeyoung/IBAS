from django.core.paginator import Paginator


# ---- get_page_object ---- #
# : 페이지네이션을 위해 Page 객체 반환하는 함수 (board, contest_board 에서 사용)
# INPUT : request, 게시판 전체 게시글 리스트, 한 페이지에 나타낼 게시글 수(default = 10)
# OUTPUT : 없음
# RETURN : Page 객체
# 작성자 : 유동현
# 마지막 수정일 : 2021.04.13
# 수정내용 :
def get_page_object(request, model_list, num_of_boards_in_one_page=10):
    paginator = Paginator(model_list, num_of_boards_in_one_page)  # 페이지네이터로 10개씩 보이게끔
    page = request.GET.get('page')  # GET 파라미터 페이지 이름
    item = paginator.get_page(page)

    return item


# ---- get_paginator_list ---- #
# : 페이지네이션을 위해 Page 객체 반환하는 함수 (board, contest_board 에서 사용)
# INPUT : request, 게시판 전체 게시글 리스트, 한 페이지에 나타낼 게시글 수(default = 10)
# OUTPUT : 없음
# RETURN : Page 객체
# 작성자 : 양태영
# 마지막 수정일 : 2021.04.08
# 수정내용 :
# 파라미터 정보
#   - request,
#   - name:"페이지의 이름",
#   - pg_list:페이지네이션 하고 싶은 쿼리셋 리스트,
#   - num: 페이지 네이션 숫자. 몇 개씩 한 페이지에 보이게 할 것인지.
def get_paginator_list(request, name, pg_list, num):
    paginator = Paginator(pg_list, num)
    page = request.GET.get(name + '_page')  # GET 파라미터 페이지 이름
    items = paginator.get_page(page)

    return items
