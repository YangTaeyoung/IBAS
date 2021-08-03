from DB.models import Board, BoardType
from django import forms
from django_summernote.widgets import SummernoteWidget


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Board
        exclude = ('board_writer', 'board_created', 'board_type_no')  # fields 또는 exclude 필수

        # ModelForm 은 pk를 일부러 사용하지 못하게 한다. 수정할 필요가 없기 때문.
        # 히든태그로 템플릿에 전달했을 때 html 개발자 도구를 통해 편집할 수 있는 가능성을 차단.
        # widgets 에 pk 인 board_no를 선언해도 템플릿에서는 인식되지 않는다.
        widgets = {
            'board_title': forms.TextInput(attrs={'placeholder': '제목을 입력하세요.'}),
            'board_cont': SummernoteWidget(),
        }

    # overriding
    def save(self, board_writer):
        # save(commit=True) 이면 1) form.cleaned_data 를 이용해 데이터 모델 객체를 생성, 2) db에 저장
        # save(commit=False) 이면 위의 1번만 실행,
        #   - default 는 commit=True
        board = super().save(commit=False)
        board.board_type_no = BoardType.objects.get(pk=4)
        board.board_writer = board_writer
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
