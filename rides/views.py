from django.shortcuts import render, HttpResponse


# Create your views here.
def rides(request):
    return render(request, 'rides/rides.html', {
        "username": request.user
        })


def hitches(request):
    return render(request, 'rides/hitches.html', {
        "username": request.user
        })


def about(request):
    return render(request, 'rides/about.html', {
        "username": request.user
        })
