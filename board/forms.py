import os
import sys
from django import forms
from DB.models import ContestBoard
from file_controller import *


class ContestForm(forms.Form):
    contest_no = forms.CharField(widget=forms.HiddenInput(), required=False)
    contest_title = forms.CharField(label="공모전 제목", max_length=100,
                                    widget=forms.TextInput(attrs={'placeholder': '공모전 이름을 입력하세요.'}))
    contest_asso = forms.CharField(label="공모전 주체 기관", max_length=100,
                                   widget=forms.TextInput(attrs={'placeholder': '주체기관을 입력하세요.'}))
    contest_topic = forms.CharField(label="공모전 주제", max_length=500,
                                    widget=forms.TextInput(attrs={'placeholder': '공모전 주제를 적어주세요.'}))
    contest_start = forms.DateTimeField(label="공모전 시작일", widget=forms.DateInput(attrs={'type': 'date'}))
    contest_deadline = forms.DateTimeField(label="공모전 마감일", widget=forms.DateInput(attrs={'type': 'date'}))
    contest_cont = forms.CharField(label="공모전 상세 설명")

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance is not None and isinstance(instance, ContestBoard):
            super().__init__(auto_id=False, initial={
                'contest_no': instance.contest_no,
                'contest_title': instance.contest_title,
                'contest_asso': instance.contest_asso,
                'contest_topic': instance.contest_topic,
                'contest_start': instance.contest_start,
                'contest_deadline': instance.contest_deadline,
                'contest_cont': instance.contest_cont,
            })
        else:
            super().__init__(auto_id=False, *args, **kwargs)

    def save(self, contest_writer):
        return ContestBoard.objects.create(
            contest_title=self.cleaned_data.get('contest_title'),
            contest_asso=self.cleaned_data.get('contest_asso'),
            contest_topic=self.cleaned_data.get('contest_topic'),
            contest_start=self.cleaned_data.get('contest_start'),
            contest_deadline=self.cleaned_data.get('contest_deadline'),
            contest_cont=self.cleaned_data.get('contest_cont'),
            contest_writer=contest_writer
        )

    def update(self):
        if self.has_changed():
            contest_no = self.cleaned_data.get('contest_no')
            contest = ContestBoard.objects.get(pk=contest_no)
            contest.contest_title = self.cleaned_data.get('contest_title')
            contest.contest_cont = self.cleaned_data.get('contest_cont')
            contest.contest_start = self.cleaned_data.get('contest_start')
            contest.contest_deadline = self.cleaned_data.get('contest_deadline')
            contest.contest_topic = self.cleaned_data.get('contest_topic')
            contest.contest_asso = self.cleaned_data.get('contest_asso')
            return contest.save()

    # overriding
    # views.py 에서 is_valid() 호출시 내부에서 자동적으로 clean 호출
    # clean 함수는
    #       1. 템플릿 폼에서 입력받은 데이터를 적절한 파이썬 type 으로 변환시켜줌.
    #       2. 위에서 정의한 input 태그에 대한 사용자 입력 값의 validation 을 검사함. 오류 발생시 내부적으로 ValidationError 발생
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


class FileForm(forms.Form):
    # exist_file = forms.FileField(widget=forms.HiddenInput(), required=False, queryset=None)
    upload_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'multiple': True,
                                      'accept': ".xlsx,.xls,image/*,.doc,.docx,video/*,.ppt,.pptx,.txt,.pdf,.py,.java"})
    )

    def save(self, instance):
        # 유효성 검사를 통해서 1개 이상의 이미지를 받을 것.
        # 이 폼은 여러개의 파일을 갖고 있을 것이다.
        # upload_new_files 이용해서 저장하기
        # contest 파일 저장할 때 이미지와 문서 분리하기..?
        upload_new_files(
            files_to_upload=self.files,
            instance=instance
        )

    # is_valid 호출 시 내부에서 자동적으로 clean 호출
    def clean(self):
        cleaned_data = super().clean()

        # 함수 호출 스택 : clean(0계층) << _clean_form(1계층) << full_clean(2계층) << errors(3계층) << is_valid(4계층)
        # 즉 is_valid 를 호출한 함수 이름을 묻는 것.
        calling_function = sys._getframe(5).f_code.co_name
        if calling_function in ['contest_register', 'contest_update']:
            if not self._check_contest_thumbnail():
                raise forms.ValidationError('공모전 이미지를 적어도 한 개 이상 등록해주세요!')

    # protected
    # contest 경우에는 이미지 파일이 항상 첫번째로 오게 해야함.
    # contest_list 에서 표지 보여줄 때 항상 첫번째로 저장되어 있는 파일을 가져오기 때문
    # 이미지 파일이 없는 경우, 보여줄 표지가 없기 때문에 오류!
    def _check_contest_thumbnail(self):
        img_ext = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

        # 로컬 저장소에 이미지 파일이 있으면 상관없음.
        # 이미지 파일은 항상 첫번째에 있기 때문에, 가장 파일만 보고 판단 가능
        for key, value in self.data:
            if 'exist_file_path' in key:
                if is_image(value):
                    return True
                else:
                    break

        files = self.files.getlist('upload_file')  # InMemoryUploadedFile 객체 리스트 (파일명으로 임시 저장되어 있음)
        for file in files:
            if is_image(file):
                return True

        return False



