from django.shortcuts import render, HttpResponse


# Create your views here.
def rides(request):
    return render(request, 'rides/rides.html')
