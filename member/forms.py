from allauth.account.utils import user_email
from django import forms
from DB.models import User, Answer, UserSchedule, UserEmail, MajorInfo
from urllib.request import urlretrieve  # 인터넷에 있는 파일 다운로드
from django.conf import settings
from user_controller import get_default_pic_path
import os


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ("user_pic", "user_gen", "user_intro", "user_apply_publish", "user_joined")
        GRADE_CHOICES = [
            (1, "1학년"),
            (2, "2학년"),
            (3, "3학년"),
            (4, "4학년")
        ]
        widgets = {
            "user_stu": forms.NumberInput(),
            "user_grade": forms.Select(choices=GRADE_CHOICES, attrs={"required": "required"}),
            "user_phone": forms.TextInput(attrs={"placeholder": "핸드폰 번호", "maxlength": 13, "required": "required"}),
            "user_name": forms.TextInput(attrs={"placeholder": "이름", "required": "required"}),
            "user_role": forms.HiddenInput(),
            "user_auth": forms.HiddenInput(),
            "user_major": forms.HiddenInput(),
        }

    def save(self, **kwargs):
        user = super().save(commit=False)
        if kwargs.get("pic_url") is not None:
            user_dir = os.path.join(settings.MEDIA_ROOT, "member", str(user.user_stu))
            try:
                os.mkdir(user_dir)
            except FileExistsError:  # 이미 동일 이름을 가진 폴더가 있는 경우
                pass
            try:
                user_pic_path = user_dir + str(user.user_stu) + ".jpg"
                urlretrieve(kwargs.get("pic_url"), user_pic_path)
                user.user_pic = user_pic_path
            except FileNotFoundError:  # 파일을 찾을 수 없는 경우.
                user.user_pic = get_default_pic_path()
            user.user_gen = UserSchedule.objects.all().first().generation
            user.save()
        return user


class UserEmailForm(forms.ModelForm):
    class Meta:
        model = UserEmail
        fields = "__all__"
        widgets = {
            "user_stu": forms.HiddenInput(),
            "provider": forms.HiddenInput(),
            "user_email": forms.HiddenInput()
        }

# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer
#         exclude = ("answer_user", "answer_created")
#         widgets = {
#             "answer_quest": forms.HiddenInput(),
#             "answer_cont": forms.Textarea(),
#         }
#
