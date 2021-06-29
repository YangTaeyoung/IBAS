from cryptography.fernet import Fernet
from DB.models import User, UserKeys
from user_controller import get_logined_user


class SimpleEnDecrypt:
    def __init__(self, request):
        if UserKeys.objects.filter(user_stu=get_logined_user(request)) is None:  # 키가 없다면
            UserKeys.objects.create(user_key=Fernet.generate_key())  # 키를 생성한다
        self.key = UserKeys.objects.filter(user_stu=get_logined_user(request))[0].user_key
        self.f = Fernet(self.key)

    def encrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.encrypt(data)  # 바이트형태이면 바로 암호화
        else:
            ou = self.f.encrypt(data.encode('utf-8'))  # 인코딩 후 암호화
        if is_out_string is True:
            return ou.decode('utf-8')  # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou

    def decrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.decrypt(data)  # 바이트형태이면 바로 복호화
        else:
            ou = self.f.decrypt(data.encode('utf-8'))  # 인코딩 후 복호화
        if is_out_string is True:
            return ou.decode('utf-8')  # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou
