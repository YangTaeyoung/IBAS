import requests
from bs4 import BeautifulSoup


# url 임베딩에 필요한 값들을 딕셔너리에 반환하는 함수
# 파라미터: 알고싶은 주소 URL
# return: {og:tag_name: value, og:tag_name: value, og:tag_name: value, og:tag_name: value} 형태로 반환
def get_og_tag(url: str):
    try:
        html = requests.get(url)
    except Exception as e:
        print(e)
        return None

    bs = BeautifulSoup(html.text, 'html.parser')
    og_property_name_list = ['title', 'description', 'url', 'image']
    result_dict = dict()
    for og_property_name in og_property_name_list:
        og_elem = bs.find('meta', property='og:'+og_property_name)
        if og_elem is not None:
            result_dict[og_property_name] = og_elem.get('content')

    return result_dict
