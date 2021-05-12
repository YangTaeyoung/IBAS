from django import forms
from django.core.exceptions import ValidationError
from django.utils.datetime_safe import date

from DB.models import Bank, BankApplyInfo, User
from IBAS.forms import FileFormBase
from django.utils.translation import gettext_lazy as _



class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ('bank_used', 'bank_title', 'bank_reason', 'bank_used_user', 'bank_plus', 'bank_minus',)

        widgets = {
            'bank_used': forms.DateInput(attrs={'type': 'date'}),
            'bank_title': forms.TextInput(attrs={'placeholder': _('제목을 입력하세요')}),
            'bank_reason': forms.TextInput(attrs={'placeholder': _("내용을 입력하세요.")}),
            'bank_used_user': forms.TextInput(attrs={'type': 'number', 'placeholder': _("회비를 사용한 부원의 학번을 입력하세요")}),
            'bank_plus': forms.NumberInput(attrs={'placeholder': _("수입액을 입력하세요")}),
            'bank_minus': forms.NumberInput(attrs={'placeholder': _("지출액을 입력하세요")}),
        }
        help_texts = {
            'bank_used': _("영수증에 명시된 사용일을 적어주세요."),
            'bank_reason': _("해당란을 입력하지 않을 시 제목과 내용이 같도록 처리합니다."),
            'bank_used_user': _("해당란을 입력하지 않을 시, 로그인 한 유저로 입력됩니다."),
            'bank_title': "",
            'bank_plus': "",
            'bank_minus': "",
        }

    def save(self, bank_cfo):
        bank = super().save(commit=False)  # db에 아직 저장하지는 않고, 객체만 생성
        bank.bank_apply = BankApplyInfo.objects.get(pk=4)
        bank.bank_cfo = bank_cfo
        if self.cleaned_data['bank_used_user'] is None:
            bank.bank_used_user = bank_cfo
        bank.save()

        return bank

    def update(self, instance):
        bank = instance
        bank.bank_used = self.cleaned_data.get('bank_used')
        bank.bank_title = self.cleaned_data.get('bank_title')
        bank.bank_used_user = User.objects.get(pk=self.cleaned_data.get('bank_used_user'))
        bank.bank_plus = self.cleaned_data.get('bank_plus')
        bank.bank_minus = self.cleaned_data.get('bank_minus')

        # 변경되지 않았으면, 쿼리를 실행하지 않음.
        if self.has_changed():
            bank.save()

        return bank

    def clean_bank_plus(self):
        income = self.cleaned_data.get('bank_plus')
        if income is None:
            return 0
        if income < 0:
            raise ValidationError(
                _('수입란에 0보다 작은 수를 입력할 수 없습니다.'),
                code='invalid'
            )
        return income

    def clean_bank_minus(self):
        outcome = self.cleaned_data.get('bank_minus')
        if outcome is None:
            return 0
        if outcome < 0:
            raise ValidationError(
                _('지출란에 0보다 작은 수를 입력할 수 없습니다.'),
                code='invalid'
            )
        return outcome

    def clean_bank_reason(self):
        reason = self.cleaned_data.get('bank_reason')
        if reason is None:
            return self.cleaned_data.get('bank_title')

        return reason

    def clean_bank_used(self):
        used_date = self.cleaned_data['bank_used']
        if used_date > date.today():
            raise ValidationError(
                _('미래 날짜를 지정할 수 없습니다!'),
                code='invalid'
            )
        return date

    def clean(self):
        if self.cleaned_data['bank_plus'] == 0 and self.cleaned_data['bank_minus'] == 0:
            raise ValidationError(
                _('수입과 지출 중 하나는 입력하세요!'),
                code='invalid'
            )


class FileForm(FileFormBase):
    upload_file = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={'multiple': True,
                   'accept': "image/*,.doc,.pdf,.hwp,.docx"})
    )
