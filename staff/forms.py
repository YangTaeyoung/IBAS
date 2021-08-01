import pytz
from django import forms
from DB.models import UserDelete, LectSchedule, UserSchedule, LectMoneyStandard, PolicyTerms, PolicyType
from django_summernote.widgets import SummernoteWidget
from date_controller import today

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


class PolicyTermsForms(forms.ModelForm):
    class Meta:
        model = PolicyTerms
        exclude = ('policy_user', 'policy_updated')
        labels = {
            "policy_title": "약관 제목",
            "policy_content": "약관 내용",
            "policy_type": "약관 종류"
        }
        widgets = {
            "policy_title": forms.TextInput(attrs={"placeholder": "약관 제목을 입력하세요."}),
            "policy_content": SummernoteWidget(),
            "policy_type": forms.HiddenInput()
        }

    def save(self, **kwargs):
        policy_terms = super().save(commit=False)
        policy_terms.policy_user = kwargs.get("policy_user")
        policy_terms.policy_updated = today()
        policy_terms.save()
        return policy_terms
