from django import forms
from DB.models import Lect, MethodInfo


class LectForm(forms.ModelForm):
    class Meta:
        model = Lect

        exclude = ("lect_chief", "lect_created", "lect_pic")
        widgets = {
            "lect_title": forms.TextInput(attrs={"placeholder": "강의 제목을 입력하세요"}),
            "lect_curri": forms.Textarea(attrs={"placeholder": "강의 계획을 작성해주세요"}),
            "lect_intro": forms.Textarea(attrs={"placeholder": "간략하게 강의를 소개해주세요"}),
            "lect_method": forms.Select(),
            "lect_place_or_link": forms.TextInput(attrs={"placeholder": "강의 방식을 먼저 선택하세요.", "disabled": "disabled"}),
            "lect_type": forms.HiddenInput(),
            "lect_deadline": forms.DateTimeInput(),
            "lect_state": forms.HiddenInput(),
            "lect_limit_num": forms.NumberInput(attrs={"placeholder": "강의 최대 수강인원수를 작성하세요. 미 작성시 무한정 수강 가능하도록 설정됩니다."}),
            "lect_reject_reason": forms.TextInput(attrs={"placeholder": "거절 사유를 입력해주세요."}),
        }

    def save(self, **kwargs):
        lect = super().save(commit=False)
        lect.lect_chief = kwargs["lect_chief"]
        lect.lect_type = self.cleaned_data.get("lect_type")
        lect.lect_state = self.cleaned_data.get("lect_state")
        lect.save()
        return lect

    def update(self, instance):
        lect = instance
        if self.has_changed():
            lect.lect_title = self.cleaned_data.get("lect_title")
            lect.lect_intro = self.cleaned_data.get("lect_intro")
            lect.lect_deadline = self.cleaned_data.get("lect_deadline")
            lect.lect_method = self.cleaned_data.get("lect_method")
            lect.lect_curri = self.cleaned_data.get("lect_curri")
            lect.lect_place_or_link = self.cleaned_data.get("lect_place_or_link")
            return lect.save()
        return lect

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("lect_method") is not None:
            cleaned_data["lect_method"] = MethodInfo.objects.get(pk=cleaned_data["lect_method"])
        return cleaned_data


class LectPicForm(forms.ModelForm):
    class Meta:
        model = Lect
        exclude = (
            "lect_chief", "lect_created", "lect_title", "lect_curri", "lect_intro", "lect_method", "lect_place_or_link",
            "lect_type", "lect_deadline", "lect_limit_num", "lect_state", "lect_reject_reason"
        )
        widgets = {
            "lect_pic": forms.FileInput(attrs={"multiple": "multiple"})
        }

    def save(self, **kwargs):
        lect = kwargs.get("instance")
        lect.lect_pic = self.cleaned_data.get("lect_pic")
        lect.save()
        return lect


class LectRejectForm(forms.ModelForm):
    class Meta:
        model = Lect

        exclude = (
            "lect_chief", "lect_created", "lect_title", "lect_curri", "lect_intro", "lect_method", "lect_place_or_link",
            "lect_pic", "lect_type",
            "lect_deadline", "lect_limit_num"
        )
        widgets = {
            "lect_state": forms.HiddenInput(),
            "lect_reject_reason": forms.TextInput(attrs={"placeholder": "거절 사유를 입력해주세요."}),
        }

    def update(self, instance):  # 강의 거절 사유를 입력했을 경우 호출되는 함수
        lect = instance
        lect.lect_state = self.cleaned_data.get("lect_state")
        lect.lect_reject_reason = self.cleaned_data.get("lect_reject_reason")

        # 변경되지 않았으면, 쿼리를 실행하지 않음.
        if self.has_changed():
            lect.save()
        return lect