from django import forms
from django.core.exceptions import ValidationError
from django.utils.datetime_safe import date, datetime
from DB.models import Bank, BankApplyInfo, User, UserRole
from IBAS.forms import FileFormBase
from django.utils.translation import gettext_lazy as _
import pytz


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

    # overriding
    # kwargs 로 bank_cfo 입력 받아야 함!
    def save(self, **kwargs):
        bank = super().save(commit=False)  # db에 아직 저장하지는 않고, 객체만 생성
        bank.bank_apply = BankApplyInfo.objects.get(pk=4)
        bank.bank_cfo = kwargs.get('bank_cfo')
        bank.save()

        return bank

    def update(self, instance):
        bank = instance
        bank.bank_used = self.cleaned_data.get('bank_used')
        bank.bank_title = self.cleaned_data.get('bank_title')
        bank.bank_used_user = self.cleaned_data.get('bank_used_user')
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
        if pytz.utc.localize(used_date) > pytz.utc.localize(datetime.today()):
            raise ValidationError(
                _('사용한 날짜를 정확히 입력해주세요!'),
                code='invalid'
            )
        return used_date

    # 수정해야함.
    def clean_bank_used_user(self):
        user = self.cleaned_data.get('bank_used_user')
        if user is None:
            user = User.objects.filter(user_role=UserRole.objects.get(pk=4)).first()

        return user

    # overriding
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
                   'accept': "image/*"})
    )

    # overriding
    # 하나 이상의 파일이 있는지 검사!
    def clean(self):
        super().clean()

        total_file_num = 0
        total_file_num += len([value for key, value in self.data.items() if "exist_file_path_" in key])
        total_file_num += len(self.cleaned_data['upload_file'])

        if total_file_num == 0:
            raise ValidationError(
                _("하나 이상의 증빙 파일을 올려주세요!"),
                code='invalid'
            )


class BankSupportForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ('bank_title', 'bank_used', 'bank_reason', 'bank_minus', 'bank_account')

        widgets = {
            'bank_used': forms.DateInput(attrs={'type': 'date'}),
            'bank_title': forms.TextInput(attrs={'placeholder': _('제목을 입력하세요')}),
            'bank_reason': forms.TextInput(attrs={'placeholder': _("지출 목적 및 사용 내역을 입력하세요.")}),
            'bank_minus': forms.NumberInput(attrs={'placeholder': _("정확한 지출액을 입력하세요")}),
            'bank_account': forms.TextInput(attrs={'placeholder': _("은행명, 계좌번호, 예금주를 입력해주세요")})
        }
        labels = {
            'bank_title': _("제목"),
            'bank_used': _("지출날짜"),
            'bank_reason': _("지출내역"),
            'bank_minus': _("지출금액"),
            'bank_account': _("입금받을 계좌"),
        }

    # overriding
    # bank_used_user 입력 받아야 함!
    def save(self, **kwargs):
        bank = super().save(commit=False)
        bank.bank_plus = 0
        bank.bank_used_user = kwargs.get('user')
        bank.bank_apply = BankApplyInfo.objects.get(pk=1)
        bank.save()

        return bank

    def update(self, instance):
        instance.bank_used = self.cleaned_data['bank_used']
        instance.bank_title = self.cleaned_data['bank_title']
        instance.bank_reason = self.cleaned_data['bank_reason']
        instance.bank_plus = 0
        instance.bank_minus = self.cleaned_data['bank_minus']
        instance.bank_account = self.cleaned_data['bank_account']
        instance.save()

        return instance

    def clean_bank_used(self):
        use_date = self.cleaned_data['bank_used']
        if pytz.utc.localize(use_date) > pytz.utc.localize(datetime.today()):
            raise ValidationError(
                _('사용한 날짜를 정확히 입력해주세요!'),
                code='invalid'
            )

        return use_date

    def clean_bank_minus(self):
        outcome = self.cleaned_data['bank_minus']
        if outcome < 0:
            raise ValidationError(
                _('지출 금액을 확인해주세요!'),
                code='invalid'
            )

        return outcome
