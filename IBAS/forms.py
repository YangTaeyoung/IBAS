from django import forms


class FileFormBase(forms.Form):
    upload_file = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={'multiple': True,
                   'accept': ".xlsx,.xls,image/*,.doc,.docx,video/*,.ppt,.pptx,.txt,.pdf,.py,.java"})
    )

    """
    [폼 객체 생성주기]
        1) (forms.py) 에서 클래스 정의
        2) (views.py) 에서 객체 생성 => 컨텍스트 변수에 담아 템플릿으로 넘겨줌
        3) (template) 폼 객체 멤버 변수는 각각 해당변수선언에 대응하는 input 태그로 변환됨.(밑에 예시)
        4) (template) 해당 템플릿에서 이탈하면 폼 객체 소멸.

    [ 변환 예시 ]          
     : 변수이름은 input 태그의 name 으로 들어감! 
     : 자동으로 required 설정됨. 안하려면 required=False 선언해야함.

    #######################################################################################
          (forms.py)            =>                   (template)
    -------------------------------------------------------------------------------------------------------------------        
    FileForm.upload_file        =>    <input type="file" name="upload_file" multiple
                                            accept=".xlsx,.xls,image/*,.doc,.docx,video/*,.ppt,.pptx,.txt,.pdf,.py,.java">
    ########################################################################################
    """

    def save(self, instance):
        # 이 폼은 여러개의 파일을 갖고 있을 것이다.
        # upload_new_files 이용해서 저장하기
        # 파일 폼 객체는 files 라는 Query dict 객체 존재  {'upload_file' : InMemoryUploadedFile 리스트}
        from file_controller import FileController
        FileController.upload_new_files(
            files_to_upload=self.cleaned_data.get('upload_file'),
            instance=instance
        )

    # overriding
    # is_valid 호출 시 내부에서 자동적으로 clean 호출
    def clean(self):
        super().clean()
        self.cleaned_data['upload_file'] = self.files.getlist('upload_file')

