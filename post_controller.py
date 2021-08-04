from DB.models import Board, ContestBoard, LectBoard, Comment, UserDelete,Lect
from django.db.models import Q


# 인스턴스를 파악해 해당 인스턴스의 덧글을 지우는 함수. 게시글을 삭제할 때 사용.
def comment_delete_by_post_delete(instance):
    comment_list = None
    if isinstance(instance, Board):
        board_ref = instance.board_no
        comment_list = Comment.objects.filter(Q(board_ref=board_ref) & Q(comment_type_id=1))
    elif isinstance(instance, ContestBoard):
        board_ref = instance.contest_no
        comment_list = Comment.objects.filter(Q(board_ref=board_ref) & Q(comment_type_id=2))
    elif isinstance(instance, LectBoard):
        board_ref = instance.lect_board_no
        comment_list = Comment.objects.filter(Q(board_ref=board_ref) & Q(comment_type_id=3))
    elif isinstance(instance, UserDelete):
        board_ref = instance.user_delete_no
        comment_list = Comment.objects.filter(Q(board_ref=board_ref) & Q(comment_type_id=4))
    if comment_list is not None:
        for comment in comment_list:
            comment.delete()
