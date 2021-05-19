from django import forms
from DB.models import Lect, MethodInfo
from user_controller import get_logined_user


class LectForm(forms.ModelForm):
    class Meta:
        model = Lect

        exclude = ("lect_chief", "lect_created")
        widgets = {
            "lect_title": forms.TextInput(attrs={"placeholder": "강의 제목을 입력하세요"}),
            "lect_curri": forms.Textarea(attrs={"placeholder": "강의 계획을 작성해주세요"}),
            "lect_intro": forms.Textarea(attrs={"placeholder": "간략하게 강의를 소개해주세요"}),
            "lect_method": forms.Select(),
            "lect_place_or_link": forms.TextInput(attrs={"placeholder": "강의 방식을 먼저 선택하세요.", "disabled": "disabled"}),
            "lect_pic": forms.FileInput(attrs={"multiple": "multiple"}),
            "lect_type": forms.HiddenInput(),
            "lect_deadline": forms.DateTimeInput(),
            "lect_state": forms.HiddenInput(),
            "lect_limit_num": forms.NumberInput(attrs={"placeholder": "강의 최대 수강인원수를 작성하세요. 미 작성시 무한정 수강 가능하도록 설정됩니다."}),
            "lect_reject_reason": forms.TextInput(attrs={"placeholder": "거절 사유를 입력해주세요."}),
        }

    def save(self, **kwargs):
        print("와?")
        lect = super().save(commit=False)
        lect.lect_chief = kwargs["lect_chief"]
        lect.lect_type = self.cleaned_data.get("lect_type")
        lect.lect_state = self.cleaned_data.get("lect_state")
        lect.save()
        return lect

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["lect_method"] = MethodInfo.objects.get(pk=cleaned_data["lect_method"])
        return cleaned_data
