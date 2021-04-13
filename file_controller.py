import shutil
from DB.models import Board, BoardFile, ContestBoard, ContestFile
import os
from IBAS.settings import MEDIA_ROOT


def get_ext(file_path):
    dot_idx = str(file_path).rfind(".")
    if dot_idx != -1:
        return str(file_path)[dot_idx:].lower()
    else:
        return str(file_path).lower()

# 파일 이름을 반환 파라미터(파일 경로)
def get_file_name(file_path):
    slash_idx = str(file_path).rfind("/")
    if slash_idx != -1:
        return str(file_path)[slash_idx + 1:]
    else:
        return str(file_path)

# 이미지인지 확인하는 함수. 파라미터(파일 경로)
def is_image(file_path):
    ext = get_ext(file_path)
    if ext == ".jpg" or ext == ".gif" or ext == ".bmp" or ext == ".png":
        return True
    else:
        return False

# 파일인지 확인 하는 함수 파라미터(파일 경로).
def is_file(file_path):
    return not is_image(file_path)


# ---- get_images_and_files_of_ ---- #
# INPUT : Board 객체 or ContestBoard 객체
# OUTPUT : 없음
# RETURN : tuple type / (게시글전체파일 리스트,게시글이미지파일 리스트,게시글문서파일 리스트)
# :
# 마지막 수정 일시 : 2021.04.13
# 작성자 : 유동현
def get_images_and_files_of_(object):
    image_list = []
    doc_list = []

    files = set()  # 쿼리셋을 담기 위한 empty Set 생성
    try:
        # Board 객체
        if isinstance(object, Board):
            files = BoardFile.objects.filter(board_no=object.board_no)
        # ContestBoard 객체
        elif isinstance(object, ContestBoard):
            files = ContestFile.objects.filter(contest_no=object.contest_no)

        else:  # 객체가 잘못 전달된 경우 / 버그로 인해서 pk가 동일한 여러개의 글이 생성된 경우 등
            raise Exception

        # 파일을 이미지 파일과 일반 문서 따로 분리
        for file in files:
            if is_image(file.file_path):
                image_list.append(file)
            else:
                doc_list.append(file)

        return files, image_list, doc_list

    # 잘못된 객체가 전달될 경우
    except Exception as error:
        print(error)  # LOGGING :: 로그 파일 생성하는 코드 나중에 수정해야 함.


# ---- delete_all_files_of_ ---- #
# INPUT : HttpRequest 객체, File 객체 리스트
# OUTPUT : 없음
# RETURN : 없음
# : 게시글 수정하는 과정에서 사용자가 제거한 파일들을 삭제함.
# 마지막 수정 일시 : 2021.04.13
# 작성자 : 유동현
def remove_files_by_user(request, files):
    for file in files:
        # exist_file_path_{파일id}가 없는 경우: 사용자가 기존에 있던 파일을 삭제하기로 결정하였음 (input tag가 없어지면서 값이 전송되지 않음)
        if request.POST.get("exist_file_path_" + str(file.file_id)) is None:
            location = os.path.join(MEDIA_ROOT, str(file.file_path))
            # 해당 파일이 존재하면 삭제 (존재하지 않는 경우 에러 발생)
            if os.path.exists(location):
                os.remove(location)  # 기존에 있던 저장소에 파일 삭제

            file.delete()  # db 기록 삭제


# ---- delete_all_files_of_ ---- #
# INPUT : Board 객체 or ContestBoard 객체
# OUTPUT : 없음
# RETURN : 없음
# : 해당 게시글의 모든 파일을 삭제한다.
# 마지막 수정 일시 : 2021.04.13
# 작성자 : 유동현
def delete_all_files_of_(obj):
    location = ''

    # Board 객체인 경우
    if isinstance(obj, Board):
        location = os.path.join(MEDIA_ROOT, 'board', str(obj.board_no))

    # ContestBoard 객체인 경우
    elif isinstance(obj, ContestBoard):
        location = os.path.join(MEDIA_ROOT, 'board', 'contest', str(obj.contest_no))

    try:
        if os.path.exists(location):  # 해당 경로가 존재하지 않는 경우에는 db 에서만 지워주면 된다.
            shutil.rmtree(location, ignore_errors=False)  # 해당 디렉토리를 포함하여 하위 폴더/파일 삭제
    except Exception as error:
        print(error)  # LOGGING :: 로그 파일 생성하는 코드 나중에 수정해야 함.


# ---- upload_new_files_of_contest ---- #
# INPUT : HttpRequest 객체, Board 또는 ContestBoard 객체
# OUTPUT : 없음
# RETURN : 없음
# : 새로 입력받은 파일들을 업로드
# 마지막 수정 일시 : 2021.04.13
# 작성자 : 유동현
def upload_new_files(request, obj):
    # 새로 사용자가 파일을 첨부한 경우
    # request.FILES 는 dict 형태 (key : value)
    # - key 는 html에서의 form 태그 name
    # - value 는 해당 form에서 전송받은 file들 / uploadedFile 객체 형태
    if "upload_file" in request.FILES:  # 넘겨받은 폼 태그 이름중에 "contest_file"이 있으면
        for file in request.FILES.getlist("upload_file"):  # 각각의 파일을 uploadedFile로 받아옴
            if isinstance(obj, ContestBoard):
                ContestFile.objects.create(
                    contest_no=ContestBoard.objects.get(pk=obj.contest_no),
                    file_path=file,  # uploadedFile 객체를 imageField 객체 할당
                    file_name=file.name.replace(' ', '_')  # imageField 객체에 의해 파일 이름 공백이 '_'로 치환되어 서버 저장
                                                           # 따라서 db 에도 이름 공백을 '_'로 치환하여 저장
                )
            elif isinstance(obj, Board):
                BoardFile.objects.create(
                    board_no=Board.objects.get(pk=obj.board_no),
                    file_path=file,  # uploadedFile 객체를 imageField 객체 할당
                    file_name=file.name.replace(' ', '_')  # imageField 객체에 의해 파일 이름 공백이 '_'로 치환되어 서버 저장
                                                           # 따라서 db 에도 이름 공백을 '_'로 치환하여 저장
                )