from django.urls import path, include
from . import views

# Media files 저장 및 전달 설정하기 위한 import
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("member/list/", views.staff_member_list, name="staff_member_list"),
    path("member/update/", views.staff_member_update, name="staff_member_update"),
    path("member/update/name/", views.user_name_update, name="member_update_name"),
    path('member/delete/list/', views.member_delete_list, name='member_delete_list'),
    path('member/delete/detail/<int:user_delete_no>', views.member_delete_detail, name='member_delete_detail'),
    path('member/delete/update/<int:user_delete_no>', views.member_delete_update, name="member_delete_update"),
    path('member/delete/delete/<int:user_delete_no>', views.member_delete_delete, name="member_delete_delete"),
    path('member/delete/register/<int:deleted_user>', views.member_delete_register, name='member_delete_register'),
    path('member/delete/decide/<int:user_delete_no>', views.member_delete_decide, name='member_delete_decide'),
    path('member/delete/aor/<int:user_delete_no>', views.member_delete_aor, name='member_delete_aor'),
    path('member/applications/', views.member_applications, name='member_applications'),
    path('member/aor/', views.member_aor, name="member_aor"),
    path('members/aor/', views.members_aor, name="members_aor"),
    path("management/",views.management, name="management"),
    path("management/update/<int:form_no>", views.management_update, name="management_update")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
