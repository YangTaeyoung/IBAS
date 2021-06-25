import requests
from bs4 import BeautifulSoup


# url 임베딩에 필요한 값들을 딕셔너리에 반환하는 함수
# 파라미터: 알고싶은 주소 URL
# return: {og:tag_name: value, og:tag_name: value, og:tag_name: value, og:tag_name: value} 형태로 반환
def get_og_tag(url: str):
    html = requests.get(url)
    bs = BeautifulSoup(html.text, 'html.parser')
    og_property_name_list = ['og:title', 'og:description', 'og:url', 'og:image']
    result_dict = dict()
    for og_property_name in og_property_name_list:
        og_elem = bs.find('meta', property=og_property_name)
        if og_elem is not None:
            result_dict[og_property_name] = og_elem.get('content')
    return result_dict
