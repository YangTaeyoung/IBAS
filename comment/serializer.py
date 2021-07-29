from django import forms
from DB.models import Comment, CommentType
from django.utils.translation import gettext_lazy as _
from user_controller import get_logined_user
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment_cont', 'comment_cont_ref')
        comment_ref_list = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.filter())
        depth = 2


    def save(self, **kwargs):
        comment = super().save(commit=False)
        request = kwargs.get("request")
        comment_type = kwargs.get("comment_type")
        comment_board_ref = kwargs.get("comment_board_ref")

        # 새로운 덧글 작성시
        if request and comment_type and comment_board_ref:

            comment.comment_writer = get_logined_user(request)
            comment.comment_type = comment_type
            comment.comment_board_ref = comment_board_ref
            comment.save()
            return comment
        # 대댓글 작성시
        elif self.validated_data.get("comment_cont_ref") is not None and request:
            comment_ref = self.validated_data.get("comment_cont_ref")
            comment.comment_board_ref = comment_ref.comment_board_ref
            comment.comment_type = comment_ref.comment_type
            comment.comment_writer = get_logined_user(request)
            comment.save()
            return comment
        else:
            pass

    def update(self, instance, validated_data):
        comment = instance

        return comment


def clean_comment_cont(self):
    pass


def clean_comment_cont_ref(self):
    pass
