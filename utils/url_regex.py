from urllib.parse import urlparse


# www. 로 시작하면 안됨.. 그래서 https:// 붙여줌.
def url_https(url):
    o = urlparse(url)
    if o.scheme == '':
        return 'https://' + url
    else:
        return url


def is_youtube(url):
    if 'https://www.youtube.com/' in url:
        return True
    else:
        return False


# url 정규표현식
url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]|" \
            r"(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"



