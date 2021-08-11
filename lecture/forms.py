from django import forms
from django.core.exceptions import ValidationError

from DB.models import Lect, MethodInfo, LectBoard, LectAssignmentSubmit
from django.utils.translation import gettext_lazy as _
from IBAS.forms import FileFormBase
from utils.url_regex import *
import re
from django_summernote.widgets import SummernoteWidget


class LectForm(forms.ModelForm):
    class Meta:
        model = Lect

        exclude = ("lect_chief", "lect_created", "lect_pic", "lect_day")
        widgets = {
            "lect_title": forms.TextInput(attrs={"placeholder": "강의 제목을 입력하세요"}),
            "lect_curri": SummernoteWidget(attrs={"placeholder": "강의 계획을 작성해주세요"}),
            "lect_intro": forms.Textarea(attrs={"placeholder": "간략하게 강의를 소개해주세요"}),
            "lect_method": forms.Select(),
            "lect_place_or_link": forms.TextInput(attrs={"placeholder": "강의 방식을 먼저 선택하세요.", "disabled": "disabled"}),
            "lect_deadline": forms.DateTimeInput(),
            "lect_limit_num": forms.NumberInput(attrs={"placeholder": "강의 최대 수강인원수를 작성하세요. 미 작성시 무한정 수강 가능하도록 설정됩니다."}),
            "lect_reject_reason": forms.TextInput(attrs={"placeholder": "거절 사유를 입력해주세요."}),
            "lect_type": forms.HiddenInput(),
            "lect_state": forms.HiddenInput(),
            "lect_paid": forms.HiddenInput()
        }

    def save(self, **kwargs):
        lect = super().save(commit=False)
        lect.lect_chief = kwargs["lect_chief"]
        lect.lect_type = self.cleaned_data.get("lect_type")
        lect.lect_state = self.cleaned_data.get("lect_state")
        if self.cleaned_data.get("lect_limit_num") is None:
            lect.lect_limit_num = 999
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
            lect.save()
            return lect
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
            "lect_type", "lect_deadline", "lect_limit_num", "lect_state", "lect_reject_reason", 'lect_day'
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
            "lect_deadline", "lect_limit_num", "lect_day"
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


# 강의 게시판 관련 기본 폼 (상속받아서 사용)
class LectBoardFormBase(forms.ModelForm):
    class Meta:
        model = LectBoard

        fields = ('lect_board_title', 'lect_board_link', 'lect_board_cont', 'lect_board_type',
                  'assignment_deadline')

        widgets = {
            'lect_board_title': forms.TextInput(attrs={"placeholder": _("제목을 입력하세요."),
                                                       "style": "font-size: 25px; height: 70px;",
                                                       "class": "form-control"}),
            'lect_board_link': forms.TextInput(attrs={"placeholder": _("강의 링크를 적어주세요."),
                                                      "class": "form-control"}),
            'lect_board_type': forms.HiddenInput(),
            'lect_board_cont': SummernoteWidget(),
            'assignment_deadline': forms.DateInput(attrs={"type": 'date',
                                                          "class": "form-control"}),
        }
        labels = {
            'lect_board_title': _("제목"),
            'lect_board_link': _("링크"),
            'lect_board_cont': _("내용"),
            'assignment_deadline': _("과제 마감일"),
        }

    def clean_lect_board_link(self):
        link = url_https(self.cleaned_data['lect_board_link'])
        if link is not None:
            reg = re.compile(url_regex)
            if reg.match(link) is None:
                raise ValidationError(
                    code='invalid',
                    message='잘못된 url 이 입력되었습니다! \n url=' + link
                )
        return link

    def save(self, **kwargs):
        lect_board = super().save(commit=False)
        lect_board.lect_board_writer = kwargs.get('lect_board_writer')
        lect_board.lect_no = kwargs.get('lect_no')
        lect_board.lect_board_ref_id = kwargs.get('lect_board_ref_id', None)

        if self.has_changed():
            lect_board.save()

        return lect_board

    def update(self, instance):
        lect_board = instance
        lect_board.lect_board_title = self.cleaned_data['lect_board_title']
        lect_board.lect_board_cont = self.cleaned_data['lect_board_cont']

        return lect_board


# 강의 게시글 폼
class LectBoardForm(LectBoardFormBase):
    class Meta(LectBoardFormBase.Meta):
        exclude = ("assignment_deadline",)

    def update(self, instance):
        lect_board = super().update(instance)
        lect_board.lect_board_link = self.cleaned_data['lect_board_link']

        if self.has_changed():
            lect_board.save()

        return lect_board


# 공지사항 폼
class LectNoticeForm(LectBoardFormBase):
    class Meta(LectBoardFormBase.Meta):
        exclude = ('lect_board_link', 'assignment_deadline')

        labels = {
            'lect_board_title': _("공지사항"),
            'lect_board_cont': _("공지 내용")
        }

    def update(self, instance):
        notice = super().update(instance)
        notice.save()


class LectAssignmentForm(LectBoardFormBase):
    class Meta(LectBoardFormBase.Meta):
        exclude = ('lect_board_link',)

        labels = {
            'lect_board_title': _('과제 제목'),
            'lect_board_cont': _('과제 내용'),
            'assignment_deadline': _('마감일')
        }

    def update(self, instance):
        assignment = super().update(instance)
        assignment.assignment_deadline = self.cleaned_data['assignment_deadline']
        assignment.save()

    def save(self, **kwargs):
        lect_board_ref = kwargs.get('lect_board_ref', None)
        if '강의 선택' in lect_board_ref or lect_board_ref is None:
            raise ValidationError(
                code='invalid',
                message=_('강의자가 과제 등록 시에는, 과제를 등록할 강의를 설정해야합니다!')
            )
        else:
            super().save(**kwargs)


# 타입에 맞는 강의 게시글 폼
def make_lect_board_form(board_type, *args, **kwargs):
    if args or kwargs:
        if board_type == 1:
            return LectNoticeForm(*args, **kwargs)
        elif board_type == 2:
            return LectBoardForm(*args, **kwargs)
        elif board_type == 3:
            return LectAssignmentForm(*args, **kwargs)
    else:
        if board_type == 1:
            return LectNoticeForm(initial={'lect_board_type': 1})
        elif board_type == 2:
            return LectBoardForm(initial={'lect_board_type': 2})
        elif board_type == 3:
            return LectAssignmentForm(initial={'lect_board_type': 3})


class AssignmentSubmitForm(forms.ModelForm):
    class Meta:
        model = LectAssignmentSubmit
        fields = ('assignment_title', 'assignment_cont')

        widgets = {
            'assignment_title': forms.TextInput(attrs={"placeholder": _("제목을 입력하세요."),
                                                       "style": "font-size: 25px; height: 70px;",
                                                       "disabled": "disabled",
                                                       "class": "form-control"}),
            'assignment_cont': SummernoteWidget,
        }

        labels = {
            'assignment_title': _('과제 제목'),
            'assignment_cont': _('과제 내용')
        }

    def save(self, **kwargs):
        submission = super().save(commit=False)
        submission.assignment_submitter = kwargs.get('assignment_submitter')
        submission.assignment_no_id = kwargs.get('lect_board_no')
        submission.lect_no_id = kwargs.get('lect_no')
        submission.save()

        return submission

    def update(self, instance):
        instance.assignment_cont = self.cleaned_data['assignment_cont']
        instance.status_id = 0  # 과제 수정하면, 기존에 통과이거나 실패였어도 대기 상태가 되어 강의가 처리 받아야함.
        instance.reject_reason = None
        instance.save()


# 이거 지우면 큰일 남
class FileForm(FileFormBase):
    pass
