"""IBAS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
# 이미지를 업로드하자
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('', include('first.urls')),
    path('user/', include('member.urls')),
    path('board/', include('board.urls')),
    path('lect/', include('lecture.urls')),
    # path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('member/', include('staff.urls')),
    path('bank/', include('bank.urls')),
    path('staff/', include('staff.urls')),
    path('my_info/', include('my_info.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('comment/', include('comment.urls')),
    # 템플릿 테스팅 링크
    path('test/add/listing/', views.add_listing, name="add_listing"),
    path('test/blog/detail/', views.blog_detail, name="blog_detail"),
    path('test/blog/standard/', views.blog_standard, name="blog_standard"),
    path('test/error/404/', views.error_404, name="error_404"),
    path('test/contact/us/', views.contact_us, name="contact_us"),
    path('test/coming/soon/', views.coming_soon, name="coming_soon"),
    path('test/index/1/', views.index_1, name="coming_soon"),
    path('test/index/2/', views.index_2, name="coming_soon"),
    path('test/index/3/', views.index_3, name="coming_soon"),
    path('test/listing/', views.listing, name="coming_soon"),
    path('test/listing/details/1/', views.listing_details, name="coming_soon"),
    path('test/listing/details/2/', views.listing_details_2, name="coming_soon"),
    path('test/listing/details/3/', views.listing_details_3, name="coming_soon"),
    path('test/listing/grid/left/sidebar/', views.listing_grid_left_sidebar, name="coming_soon"),
    path('test/listing/grid/right/sidebar/', views.listing_grid_right_sidebar, name="coming_soon"),
    path('test/listing/grid/map/left/sidebar/', views.listing_grid_map_left_sidebar, name="coming_soon"),
    path('test/listing/grid/map/right/sidebar/', views.listing_grid_map_right_sidebar, name="coming_soon"),
    path('test/listing/left/sidebar/', views.listing_left_sidebar, name="coming_soon"),
    path('test/listing/right/sidebar/', views.listing_right_sidebar, name="coming_soon"),
    path('test/register', views.register, name="coming_soon"),
]
# 이미지 URL 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
