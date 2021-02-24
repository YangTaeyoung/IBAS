from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.lect_list, name="lect_list"),
    # path("list/i/", views.lect_my_list, name="lect_my_list"),
    path("register/", views.lect_register, name="lect_register"),
    path("update/", views.lect_update, name="lect_update"),
    path("delete/", views.lect_delete, name="lect_delete"),
    # path("ask/list", views.lect_ask_list, name="lect_ask_list"),
    # path("aor/", views.lect_apply_or_reject, name="lect_apply_or_reject"),
    # path("board/room/", views.lect_board_room, name="lect_board_room"),
    # path("board/register/", views.lect_board_register, name="lect_board_register"),
    # path("board/update/", views.lect_board_update, name="lect_board_update"),
    # path("board/delete/", views.lect_board_delete, name="lect_board_delete"),
    # path("board/detail/", views.lect_board_detail, name="lect_board_detail"),
    # path("assign/register/", views.lect_assign_register, name="lect_assign_register"),
    # path("assign/update/", views.lect_assign_update, name="lect_assign_update"),
    # path("assign/delete/", views.lect_assign_delete, name="lect_assign_delete"),

]
