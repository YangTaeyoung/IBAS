def get_ext(file_path):
    dot_idx = str(file_path).rfind(".")
    if dot_idx != -1:
        return str(file_path)[dot_idx:].lower()
    else:
        return str(file_path).lower()


def get_file_name(file_path):
    slash_idx = str(file_path).rfind("/")
    if slash_idx != -1:
        return str(file_path)[slash_idx + 1:]
    else:
        return str(file_path)


def is_image(file_path):
    ext = get_ext(file_path)
    if ext == ".jpg" or ext == ".gif" or ext == ".bmp" or ext == ".png":
        return True
    else:
        return False


def is_file(file_path):
    return not is_image(file_path)
