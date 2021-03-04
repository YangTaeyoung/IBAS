def get_filename_with_ext(path):
    return path.rsplit('/')[0]


def get_filename(filename):
    return filename[0:filename.rindex(".")]


def get_ext(path_or_filename):
    return path_or_filename.rsplit(".")[0]
