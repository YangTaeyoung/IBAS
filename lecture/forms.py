from django import forms
from DB.models import Lect, MethodInfo, LectBoard, LectBoardType, LectAssignment
from django.utils.translation import gettext_lazy as _
from IBAS.forms import FileFormBase
from user_controller import get_logined_user


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


class LectBoardFormBase(forms.ModelForm):
    class Meta:
        model = LectBoard

        fields = ('lect_board_title', 'lect_board_link', 'lect_board_cont', 'lect_board_type_no')

        widgets = {
            'lect_board_title': forms.TextInput(attrs={"placeholder": _("제목을 입력하세요."),
                                                       "style": "font-size: 25px; height: 70px;"}),
            'lect_board_link': forms.TextInput(attrs={"placeholder": _("강의 링크를 적어주세요.")}),
            'lect_board_type_no': forms.HiddenInput(),
            'lect_board_cont': forms.TextInput(),
        }
        labels = {
            'lect_board_title': _("강의 제목"),
            'lect_board_link': _("강의 링크"),
            'lect_board_cont': _("내용"),
        }

    def save(self, **kwargs):
        lect_board = super().save(commit=False)
        lect_board.lect_board_writer = kwargs.get('lect_board_writer')
        lect_board.lect_no = kwargs.get('lect_no')

        if self.has_changed():
            lect_board.save()

        return lect_board

    def update(self, instance):
        lect_board = instance
        lect_board.lect_board_title = self.cleaned_data['lect_board_title']
        lect_board.lect_board_cont = self.cleaned_data['lect_board_cont']

        return lect_board


class LectBoardForm(LectBoardFormBase):
    class Meta(LectBoardFormBase.Meta):
        pass

    def update(self, instance):
        lect_board = super().update(instance)
        lect_board.lect_board_link = self.cleaned_data['lect_board_link']

        if self.has_changed():
            lect_board.save()

        return lect_board


class LectNoticeForm(LectBoardFormBase):
    class Meta(LectBoardFormBase.Meta):
        exclude = ('lect_board_link', )

        labels = {
            'lect_board_title': _("공지사항"),
            'lect_board_cont': _("공지 내용")
        }

    def update(self, instance):
        notice = super().update(instance)
        notice.save()


def make_lect_board_form(board_type, *args, **kwargs):
    if args or kwargs:
        if board_type == 1:
            return LectNoticeForm(*args, **kwargs)
        elif board_type == 2:
            return LectBoardForm(*args, **kwargs)
    else:
        if board_type == 1:
            return LectNoticeForm(initial={'lect_board_type_no': 1})
        elif board_type == 2:
            return LectBoardForm(initial={'lect_board_type_no': 2})


class LectAssignmentForm(forms.ModelForm):
    class Meta:
        model = LectAssignment

        fields = ('lect_assignment_title', 'lect_assignment_cont', 'lect_assignment_deadline')

        widgets = {
            'lect_assignment_title': forms.TextInput(attrs={"placeholder": _("과제 제목을 입력하세요."),
                                                       "style": "font-size: 25px; height: 70px;"}),
            'lect_assignment_cont': forms.TextInput(),
            'lect_assignment_deadline': forms.DateInput(attrs={'type': 'date'}),
        }

        labels = {
            'lect_assignment_title': _("과제 제목"),
            'lect_assignment_cont': _("과제 내용"),
            'lect_assignment_deadline': _("마감일")
        }

    def save(self, **kwargs):
        lect_assignment = super().save(commit=False)
        lect_assignment.lect_assignment_writer = kwargs.get('lect_assignment_writer')
        lect_assignment.lect_board_no = kwargs.get('lect_board_no')
        lect_assignment.save()

        return lect_assignment

    def update(self, instance):
        assignment = instance
        assignment.lect_assignment_title = self.cleaned_data['lect_assignment_title']
        assignment.lect_assignment_cont = self.cleaned_data['lect_assignment_cont']
        assignment.lect_assignment_deadline = self.cleaned_data['lect_assignment_deadline']

        if self.has_changed():
            assignment.save()

        return assignment


# 이거 지우면 큰일 남
class FileForm(FileFormBase):
    pass


class AssignmentFileForm(forms.Form):
    assignment_file = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={'multiple': True,
                   'accept': ".xlsx,.xls,image/*,.doc,.docx,video/*,.ppt,.pptx,.txt,.pdf,.py,.java"})
    )

    def save(self, instance):
        from file_controller import FileController
        FileController.upload_new_files(
            files_to_upload=self.cleaned_data.get('assignment_file'),
            instance=instance
        )

    # overriding
    # is_valid 호출 시 내부에서 자동적으로 clean 호출
    def clean(self):
        super().clean()
        self.cleaned_data['assignment_file'] = self.files.getlist('assignment_file')




