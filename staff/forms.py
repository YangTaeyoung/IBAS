from django import forms
from DB.models import UserDelete, LectSchedule, UserSchedule, LectMoneyStandard

DATETIME_LOCAL_FORMAT = "%Y-%m-%dT%H:%M"

class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = UserDelete

        exclude = ("user_delete_created", "suggest_user")

        widgets = {
            "user_delete_title": forms.TextInput(attrs={"placeholder": "제목을 입력하세요"}),
            "user_delete_content": forms.Textarea(),
            "deleted_user": forms.HiddenInput(),
            "user_delete_state": forms.HiddenInput()
        }

    def save(self, **kwargs):
        user_delete = super().save(commit=False)
        user_delete.suggest_user = kwargs.get("suggest_user")
        user_delete.save()
        return user_delete

    def update(self, instance: UserDelete):
        user_delete = instance
        if self.has_changed():
            user_delete.user_delete_title = self.cleaned_data.get('user_delete_title')
            user_delete.user_delete_content = self.cleaned_data.get('user_delete_content')
            return user_delete.save()
        return user_delete


class UserScheduleForm(forms.ModelForm):
    class Meta:
        model = UserSchedule
        exclude = tuple()
        widgets = {
            "generation": forms.NumberInput(),
            "user_register_start": forms.DateTimeInput(format=DATETIME_LOCAL_FORMAT),
            "user_register_end": forms.DateTimeInput(format=DATETIME_LOCAL_FORMAT),
            "user_interview_start": forms.DateInput(),
            "user_interview_end": forms.DateInput(),
            "result_announce_date": forms.DateTimeInput(format=DATETIME_LOCAL_FORMAT)
        }


class LectScheduleForm(forms.ModelForm):
    class Meta:
        model = LectSchedule
        fields = "__all__"
        widgets = {
            "lect_register_start": forms.DateTimeInput(format=DATETIME_LOCAL_FORMAT),
            "lect_register_end": forms.DateTimeInput(format=DATETIME_LOCAL_FORMAT),
        }


class LectMoneyStandardForm(forms.ModelForm):
    class Meta:
        model = LectMoneyStandard
        fields = "__all__"
        widgets = {
            "money_1to5": forms.NumberInput(),
            "money_6to10": forms.NumberInput(),
            "money_11to20": forms.NumberInput(),
            "money_21over": forms.NumberInput()
        }
