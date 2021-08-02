from django.urls import path
from . import views

urlpatterns = [
    path('<str:type>/register/<int:board_ref>',views.comment_register, name="comment_register"),
    path('register/<int:comment_id>', views.comment_ref_register, name="comment_ref_register"),
    path('update/<int:comment_id>', views.comment_update, name="comment_update"),
    path('delete/<int:comment_id>', views.comment_delete, name="comment_delete"),
    # path('<int:type_no>/view/<int:board_ref>', views.comment_view, name="comment_view"),
    path('<str:type>/view/<int:board_ref>', views.axios_response, name="comment_view")
]