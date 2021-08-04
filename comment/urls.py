from django.urls import path
from . import views

urlpatterns = [
    path('<str:type>/register/<int:board_ref>', views.comment_register, name="comment_register"),
    path('update/<int:comment_id>', views.comment_update, name="comment_update"),
    path('delete/<int:comment_id>', views.comment_delete, name="comment_delete"),
    path('<str:type>/view/<int:board_ref>', views.comment_view, name="comment_view"),
]