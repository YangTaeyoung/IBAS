from django.shortcuts import render
from user_controller import get_logined_user
from DB.models import UserDelete

# def comment_register(request):
#     comment_base_dict = {
#         "comment_cont": request.POST.get('comment_cont'),
#         "comment_wrtier": get_logined_user(request),
#     }
#     if request.POST.get("comment_cont_ref") is not None:
#         comment_base_dict.update(comment_cont_ref=request.POST.get("comment_cont_ref"))
#
#     if request.POST.get('user_delete_no') is not None:
#         comment_base_dict.update(user_delete_no=UserDelete.objects.get(pk=request.POST.get("user_delete_no")))
#         UserDeleteComment.objects.create(comment_base_dict)



def add_listing(request):
    context = {}
    return render(request, "add-listing.html", context)


def blog_detail(request):
    context = {}
    return render(request, "blog-details.html", context)


def blog_standard(request):
    context = {}
    return render(request, "blog-standard.html", context)


def coming_soon(request):
    context = {}
    return render(request, "coming-soon.html", context)


def contact_us(request):
    context = {}
    return render(request, "contact-us.html", context)


def error_404(request):
    context = {}
    return render(request, "error-404.html", context)


def index_1(request):
    context = {}
    return render(request, "index-1.html", context)


def index_2(request):
    context = {}
    return render(request, "index-2.html", context)


def index_3(request):
    context = {}
    return render(request, "index-3.html", context)


def listing(request):
    context = {}
    return render(request, "listing.html", context)


def listing_details(request):
    context = {}
    return render(request, "listing-details.html", context)


def listing_details_2(request):
    context = {}
    return render(request, "listing-details-2.html", context)


def listing_details_3(request):
    context = {}
    return render(request, "listing-details-3.html", context)


def listing_grid_left_sidebar(request):
    context = {}
    return render(request, "listing-grid-left-sidebar.html", context)


def listing_grid_map_left_sidebar(request):
    context = {}
    return render(request, "listing-grid-map-left-sidebar.html", context)


def listing_grid_map_right_sidebar(request):
    context = {}
    return render(request, "listing-grid-map-right-sidebar.html", context)


def listing_grid_right_sidebar(request):
    context = {}
    return render(request, "listing-grid-map-right-sidebar.html", context)


def listing_left_sidebar(request):
    context = {}
    return render(request, "listing-left-sidebar.html", context)


def listing_right_sidebar(request):
    context = {}
    return render(request, "listing-right-sidebar.html", context)


def register(request):
    context = {}
    return render(request, "register_1.html", context)
