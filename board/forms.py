# forms.py

from django import forms
from DB.models import Board

from django_summernote.widgets import SummernoteWidget


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['board_title', 'board_content']
        widgets = {
            'content': SummernoteWidget(),
        }

