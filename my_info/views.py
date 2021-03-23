from django.shortcuts import render

# Create your views here.
def my_info_top(request):
    context = {}
    return render(request, 'my_info_top.html', context) #