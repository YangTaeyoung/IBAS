from django import forms
from DB.models import UserDelete


class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = UserDelete

        exclude = ("user_delete_created", "suggest_user")

        widgets = {
            "user_delete_title": forms.TextInput(attrs={"placeholder": "제목을 입력하세요"}),
            "user_delete_content": forms.Textarea(),
            "deleted_user": forms.HiddenInput(),
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
