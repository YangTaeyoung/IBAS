from django.shortcuts import render

# Create your views here.
def my_info(request):
    context = {}
    return render(request, 'my_info.html', context) #