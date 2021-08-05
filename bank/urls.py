from django.urls import path, include
from . import views
# Media files 저장 및 전달 설정하기 위한 import
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('list/', views.bank, name='bank_list'),  # 회계 게시판 작업
    path('delete/<int:bank_no>/', views.bank_delete, name='bank_delete'),
    path('update/<int:bank_no>/', views.bank_update, name='bank_update'),
    path('register/', views.bank_register, name='bank_register'),
    path('lecture/summary/', views.bank_lecture_summary, name="bank_lecture_summary"),
    path("lecture/summary/update", views.bank_lecture_summary_update, name="bank_lecture_summary_update"),
    path('support/board/', views.bank_support_board, name='bank_support_board'),  # 회계 게시판 목록
    path('support/register/', views.bank_support_register, name='bank_support_register'),  # 회계 게시판 목록
    path('support/detail/<int:bank_no>', views.bank_support_detail, name='bank_support_detail'),  # 회계 게시판 목록
    path('support/aor/<int:bank_no>', views.bank_support_aor, name='bank_support_aor'),
    path('support/delete/<int:bank_no>', views.bank_support_delete, name="bank_support_delete"),
    path('support/update/<int:bank_no>', views.bank_support_update, name="bank_support_update"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
