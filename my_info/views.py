from django.shortcuts import render

# Create your views here.

def my_info(request):
    return render(request, 'my_post.html')