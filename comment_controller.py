from DB.models import Comment
from django.db.models import Q
from comment.serializer import CommentSerializer


def get_comment_list(comment_type_no: int, comment_board_ref: int):
    comment_list = Comment.objects.filter(
        Q(comment_type__comment_type_no=comment_type_no) & Q(comment_board_ref=comment_board_ref) & Q(
            comment_cont_ref__isnull=True)).prefetch_related("comment_ref").order_by("-comment_created")

    return CommentSerializer(comment_list)
