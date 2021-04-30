import sys
from django import forms
from IBAS.forms import FileFormBase, FileController
from file_controller import *


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        exclude = ('board_writer', 'board_created',)  # fields 또는 exclude 필수
        widgets = {
            'board_no': forms.HiddenInput(),
            'board_type_no': forms.HiddenInput(),
            'board_title': forms.TextInput(attrs={'placeholder': '제목을 입력하세요.'}),
            'board_cont': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        board_type_no = kwargs.get('board_type_no')
        instance = kwargs.get('instance')

        if board_type_no is not None:
            super().__init__(auto_id=False, initial={'board_type_no': board_type_no})

        elif instance is not None and isinstance(instance, Board):
            super().__init__(instance=instance)

        else:
            super().__init__(auto_id=False, *args, **kwargs)

    def save(self, board_writer):
        board = super().save(commit=False)
        board.board_type_no = self.cleaned_data.get('board_type_no')
        board.board_writer = board_writer
        board.save()

        return board

    def update(self, pk):
        board = Board.objects.get(pk=pk)
        board.board_title = self.cleaned_data.get('board_title')
        board.board_cont = self.cleaned_data.get('board_cont')

        if self.has_changed():
            board.save()

        return board


class ContestForm(forms.ModelForm):
    class Meta:
        model = ContestBoard
        # fields = '__all__'
        exclude = ('contest_writer', 'contest_created')  # fields 또는 exclude 필수
        widgets = {
            'contest_title': forms.TextInput(attrs={'placeholder': '공모전 이름을 입력하세요.'}),
            'contest_asso': forms.TextInput(attrs={'placeholder': '주최기관을 입력하세요.'}),
            'contest_topic': forms.TextInput(attrs={'placeholder': '공모전 주제를 적어주세요.'}),
            'contest_start': forms.DateInput(attrs={'type': 'date'}),
            'contest_deadline': forms.DateInput(attrs={'type': 'date'}),
            'contest_cont': forms.Textarea(),
        }
        labels = {
            'contest_title': '공모전 제목',
            'contest_asso': '공모전 주최기관',
            'contest_topic': '공모전 주제',
            'contest_start': '공모전 시작일',
            'contest_deadline': '공모전 마감일',
            'contest_cont': '공모전 상세 설명',
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance is not None and isinstance(instance, ContestBoard):
            super().__init__(instance=instance)
        else:
            super().__init__(*args, **kwargs)

    def save(self, contest_writer):
        contest = super().save(commit=False)  # db에 아직 저장하지는 않고, 객체만 생성
        contest.contest_writer = contest_writer  # 유저정보 받고
        contest.save()  # db에 저장

        return contest

    def update(self, pk):
        contest = ContestBoard.objects.get(pk=pk)
        contest.contest_title = self.cleaned_data.get('contest_title')
        contest.contest_cont = self.cleaned_data.get('contest_cont')
        contest.contest_start = self.cleaned_data.get('contest_start')
        contest.contest_deadline = self.cleaned_data.get('contest_deadline')
        contest.contest_topic = self.cleaned_data.get('contest_topic')
        contest.contest_asso = self.cleaned_data.get('contest_asso')

        if self.has_changed():
            contest.save()

        return contest

    def clean(self):
        cleaned_data = super().clean()
        start_date = self.cleaned_data.get('contest_start')
        finish_date = self.cleaned_data.get('contest_deadline')

        errors = []
        if not start_date <= finish_date:
            errors.append(forms.ValidationError('공모전 시작일과 마감일을 확인해주세요!'))

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data


class FileForm(FileFormBase):
    # overriding
    def save(self, instance):
        # 이 폼은 여러개의 파일을 갖고 있을 것이다.
        # upload_new_files 이용해서 저장하기
        # 파일 폼 객체는 files 라는 Query dict 객체 존재  {'upload_file' : InMemoryUploadedFile 리스트}
        upload_new_files(
            files_to_upload=self.cleaned_data.get('upload_file'),
            instance=instance
        )

    # overriding
    # is_valid 호출 시 내부에서 자동적으로 clean 호출
    def clean(self):
        super().clean()
        self.cleaned_data['upload_file'] = self.files.getlist('upload_file')

        # 호출 함수 이름 반환 : sys._getframe(5).f_code.co_name
        # 함수 호출 스택 : clean(0계층, 현재 함수) << _clean_form(1계층) << full_clean(2계층) << errors(3계층) << is_valid(4계층)
        # 즉 is_valid 를 호출한 함수 이름을 묻는 것.
        calling_function = sys._getframe(5).f_code.co_name

        if calling_function in ['contest_register', 'contest_update']:
            if not self._check_contest_thumbnail():
                self.cleaned_data['upload_file'] = None
                raise forms.ValidationError('공모전 이미지를 적어도 한 개 이상 등록해주세요!')

    # protected
    # contest 경우에는 이미지 파일이 항상 첫번째로 오게 해야함.
    # contest_list 에서 표지 보여줄 때 항상 첫번째로 저장되어 있는 파일을 가져오기 때문
    # 이미지 파일이 없는 경우, 보여줄 표지가 없기 때문에 오류!
    def _check_contest_thumbnail(self):
        # 로컬 저장소에 이미지 파일이 있으면 상관없음.
        # 이미지 파일은 항상 첫번째에 있기 때문에, 가장 파일만 보고 판단 가능
        for key, value in self.data.items():
            if 'exist_file_path' in key:
                if is_image(value):
                    return True
                else:
                    break

        # 파일 폼 객체는 files 라는 Query dict 객체 존재  {'upload_file' : InMemoryUploadedFile 리스트}
        # InMemoryUploadedFile 객체 (장고에 의해 파일명으로 임시 저장되어 있음)
        files = self.files.getlist('upload_file')
        for file in files:
            if is_image(file):
                return True

        return False
