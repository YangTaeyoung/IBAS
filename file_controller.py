def is_image(file_path):
    ext = str(file_path).rsplit(".")[0]
    if ext == "jpg" or ext == "gif" or ext == "bmp" or ext == "png":
        return True
    else:
        return False
