# 내부 호출용 함수
# 유투브 URL뒷부분을 넣으면 iframe 태그를 반환해줌
# 사용시에는 autoescape off를 사용하고 쓸 것.
def get_youtube_tag(behind_of_url):
    return  '<iframe width="560" height="315" ' \
            'src="https://www.youtube.com/embed/' + behind_of_url + '"' \
            ' title="YouTube video player"' \
            ' frameborder="0"' \
            ' allow="accelerometer; ' \
            'autoplay; ' \
            'clipboard-write; ' \
            'encrypted-media; ' \
            'gyroscope; ' \
            'picture-in-picture" allowfullscreen>' \
            '</iframe>'


# 유투브 url을 넣으면 iframe 태그를 반환하는 함수
# 사용시에는 autoescape off를 사용하고 쓸 것.
def get_youtube(url: str):
    equal_idx = url.rfind('=')
    slash_idx = url.rfind('/')
    if equal_idx != -1:
        youtube_url = url[equal_idx+1:]
        return get_youtube_tag(youtube_url)
    if slash_idx != -1:
        youtube_url = url[slash_idx+1:]
        return get_youtube_tag(youtube_url)
