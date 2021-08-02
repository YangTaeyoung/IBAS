from django.urls import path
from comment import views

urlpatterns = [
    path('', views.axios_response, name="axios_response"),

    path('update/', views.update, name="comment_update"),
    path('delete/', views.comment_delete, name="comment_delete"),
    path('register/', views.comment_register, name="comment_register"),
]
