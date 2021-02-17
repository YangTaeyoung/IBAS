from django.shortcuts import render


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
    return render(request, "top_bar.html", context)


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
    return render(request, "register.html", context)
