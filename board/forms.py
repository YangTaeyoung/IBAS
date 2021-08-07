import sys
from django import forms
from IBAS.forms import FileFormBase
from file_controller import FileController
from DB.models import Board, ContestBoard
from django.utils.translation import gettext_lazy as _
from django_summernote.widgets import SummernoteWidget


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        exclude = ('board_writer', 'board_created', 'board_fixdate')  # fields 또는 exclude 필수

        # ModelForm 은 pk를 일부러 사용하지 못하게 한다. 수정할 필요가 없기 때문.
        # 히든태그로 템플릿에 전달했을 때 html 개발자 도구를 통해 편집할 수 있는 가능성을 차단.
        # widgets 에 pk 인 board_no를 선언해도 템플릿에서는 인식되지 않는다.
        widgets = {
            'board_type_no': forms.HiddenInput(),
            'board_title': forms.TextInput(attrs={'placeholder': _('제목을 입력하세요.')}),
            'board_cont': SummernoteWidget(),
        }

    # overriding
    # kwargs 로 board_writer 꼭 받아야함.
    def save(self, **kwargs):
        # save(commit=True) 이면 1) form.cleaned_data 를 이용해 데이터 모델 객체를 생성, 2) db에 저장
        # save(commit=False) 이면 위의 1번만 실행,
        #   - default 는 commit=True
        board = super().save(commit=False)
        board.board_type_no = self.cleaned_data.get('board_type_no')
        board.board_writer = kwargs.get('board_writer')
        if kwargs.get('board_fixdate') is not None:
            board.board_fixdate = kwargs.get('board_fixdate')
        board.save()

        return board

    # board 객체를 넘겨 받고, 내용 수정 후 저장
    def update(self, instance):
        board = instance
        board.board_title = self.cleaned_data.get('board_title')
        board.board_cont = self.cleaned_data.get('board_cont')

        # 변경되지 않았으면, 쿼리를 실행하지 않음.
        if self.has_changed():
            board.save()

        return board


class ContestForm(forms.ModelForm):
    class Meta:
        model = ContestBoard
        # fields = '__all__'
        exclude = ('contest_writer', 'contest_created')  # fields 또는 exclude 필수
        # ModelForm 은 pk를 일부러 사용하지 못하게 한다. 수정할 필요가 없기 때문.
        # 히든태그로 템플릿에 전달했을 때 html 개발자 도구를 통해 편집할 수 있는 가능성을 차단.
        # widgets 에 pk 인 contest_no를 선언해도 템플릿에서는 인식되지 않는다.
        widgets = {
            'contest_title': forms.TextInput(attrs={'placeholder': _('공모전 이름을 입력하세요.')}),
            'contest_asso': forms.TextInput(attrs={'placeholder': _('주최기관을 입력하세요.')}),
            'contest_topic': forms.TextInput(attrs={'placeholder': _('공모전 주제를 적어주세요.')}),
            'contest_start': forms.DateInput(attrs={'type': 'date'}),
            'contest_deadline': forms.DateInput(attrs={'type': 'date'}),
            'contest_cont': forms.Textarea(),
        }
        labels = {
            'contest_title': _('공모전 제목'),
            'contest_asso': _('공모전 주최기관'),
            'contest_topic': _('공모전 주제'),
            'contest_start': _('공모전 시작일'),
            'contest_deadline': _('공모전 마감일'),
            'contest_cont': _('공모전 상세 설명'),
        }

    # overriding
    # kwargs 로 contest_writer 꼭 받아야함.
    def save(self, **kwargs):
        contest = super().save(commit=False)  # db에 아직 저장하지는 않고, 객체만 생성
        contest.contest_writer = kwargs.get('contest_writer')  # 유저정보 받고
        contest.save()  # db에 저장

        return contest

    # contest 객체를 넘겨 받고, 수정된 내용을 저장
    def update(self, instance):
        contest = instance
        contest.contest_title = self.cleaned_data.get('contest_title')
        contest.contest_cont = self.cleaned_data.get('contest_cont')
        contest.contest_start = self.cleaned_data.get('contest_start')
        contest.contest_deadline = self.cleaned_data.get('contest_deadline')
        contest.contest_topic = self.cleaned_data.get('contest_topic')
        contest.contest_asso = self.cleaned_data.get('contest_asso')

        # 변경되지 않았으면, 쿼리를 실행하지 않음.
        if self.has_changed():
            contest.save()

        return contest

    # overriding
    def clean(self):
        cleaned_data = super().clean()
        start_date = self.cleaned_data.get('contest_start')
        finish_date = self.cleaned_data.get('contest_deadline')

        errors = []
        if not start_date <= finish_date:
            errors.append(forms.ValidationError(
                _('공모전 시작일과 마감일을 확인해주세요!'),
                code='invalid'
            ))

        if errors:
            raise forms.ValidationError(errors)


class FileForm(FileFormBase):
    # overriding
    # is_valid 호출 시 내부에서 자동적으로 clean 호출
    def clean(self):
        super().clean()

        # 호출 함수 이름 반환 : sys._getframe(5).f_code.co_name
        # 함수 호출 스택 : clean(0계층, 현재 함수) << _clean_form(1계층) << full_clean(2계층) << errors(3계층) << is_valid(4계층)
        # 즉 is_valid 를 호출한 함수 이름을 묻는 것.
        calling_function = sys._getframe(5).f_code.co_name

        if calling_function in ['contest_register', 'contest_update', 'activity_register', 'activity_update']:
            # 이미지 파일이 없는 경우
            if not self._check_contest_thumbnail():
                print("이미지 있니?", self._check_contest_thumbnail())
                self.cleaned_data['upload_file'] = None  # cleaned_data 를 비운다
                raise forms.ValidationError(
                    _('공모전 이미지를 적어도 한 개 이상 등록해주세요!'),
                    code='invalid'
                )

    # protected
    def _check_contest_thumbnail(self):
        for key, value in self.data.items():
            # request 를 통해 넘겨받은 데이터 중,
            # exist_file_path 라는 문자열을 포함한 id 값이 있으면,
            # 해당 value 는 파일 이름이므로, 확장자가 이미지 파일인지 검사한다.
            # 이미지 파일이 하나라도 있으면 괜춘!
            if 'exist_file_path' in key:
                # 이미지가 있으면 괜춘!
                if FileController.is_image(value):
                    return True

        # 파일 폼 객체는 files 라는 Query dict 객체 존재  {'upload_file' : InMemoryUploadedFile 리스트}
        # InMemoryUploadedFile 객체 (장고에 의해 파일명으로 임시 저장되어 있음)
        files = self.files.getlist('upload_file')
        for file in files:
            if FileController.is_image(file):
                return True

        return False
